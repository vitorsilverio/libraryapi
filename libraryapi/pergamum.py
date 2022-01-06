import re
from io import BytesIO
from itertools import chain
from typing import Dict
from typing import Optional

from pydantic import BaseModel
from pydantic.error_wrappers import ValidationError
from pymarc import Field  # type: ignore
from pymarc import Record  # type: ignore
from pymarc.marcxml import record_to_xml  # type: ignore
from requests import Session  # type: ignore
from requests.exceptions import HTTPError  # type: ignore
from xmltodict import parse  # type: ignore
from zeep import Client
from zeep.exceptions import XMLSyntaxError
from zeep.transports import Transport


class PergamumWebServiceException(Exception):
    def __init__(self, message: str) -> None:
        self.message = message


class DadosMarc(BaseModel):
    """Represents a Dados_marc object received from Pergamum Web Service"""

    paragrafo: list[str]
    indicador: list[Optional[str]]
    descricao: list[Optional[str]]


class PergamumWebServiceRequest:
    """Represents a connection that make requests to Pergamum Web Service"""

    def __init__(self, base_url: str) -> None:
        session = Session()
        session.headers.update({"Accept-Encoding": "identity"})
        try:
            self.client = Client(
                f"{base_url}/web_service/servidor_ws.php?wsdl",
                transport=Transport(session=session),
            )
        except HTTPError as e:
            raise PergamumWebServiceException(
                message=f"{base_url}/web_service/servidor_ws.php?wsdl returned {e.response.status_code}"
            )
        except XMLSyntaxError:
            raise PergamumWebServiceException(
                "Invalid response from Pergamum WebService."
            )

    def busca_marc(self, cod_acervo: int) -> str:
        return self.client.service.busca_marc(codigo_acervo_temp=cod_acervo)


class Conversor:
    """Transform the data retrieved by the Pergamum Web Service "busca_marc"
    request to Pymarc Fields and Records"""

    @staticmethod
    def build_field(paragrafo, indicador, descricao) -> Field:
        # Indicators handling:
        # Default indicators are "\\" (2 empty spaces).
        # Pergamum WS returns indicators as:
        # - ' X X '
        # - 'X X '
        # - 'X X'
        # and more.
        # Logic here consists removing trailing space and get the last char
        # as the second indicator and the last -2 char as first indicator.

        indicators = [" ", " "]
        if indicador:
            indicador = indicador.rstrip()
            if len(indicador.rstrip()) <= 2:
                indicators[0] = indicador.strip()
            else:
                indicators[0] = indicador[-3]
                indicators[1] = indicador[-1]

        # Subfields handling:
        # Split the contents at "$", ignoring the first one to avoid the
        # creation of an empty segment. Split them again getting the first
        # position as the subfield code and the rest as the value.

        subfields = (
            list(
                chain.from_iterable(
                    [[s[0], s[2:].strip()] for s in descricao[1:].split("$")]
                )
            )
            if descricao
            else None
        )

        return Field(
            tag=paragrafo.strip(),
            indicators=indicators,
            subfields=subfields,
            data=descricao.replace("#", " ")
            if int(paragrafo) < 10
            else "",  # Only control fields has "data" param
        )

    @staticmethod
    def convert_dados_marc_to_record(dados_marc: DadosMarc, id: int) -> Record:
        record = Record(leader="     nam a22      a 4500")

        for paragrafo, indicador, descricao in zip(
            dados_marc.paragrafo, dados_marc.indicador, dados_marc.descricao
        ):
            if not descricao:
                descricao = ""
            if indicador and "<br>" in indicador:
                for indicador, descricao in zip(
                    indicador.split("<br>"), descricao.split("<br>")
                ):
                    record.add_field(
                        Conversor.build_field(paragrafo, indicador, descricao)
                    )
            elif descricao and "<br>" in descricao:
                for descricao in descricao.split("<br>"):
                    record.add_field(
                        Conversor.build_field(paragrafo, indicador, descricao)
                    )
            else:
                record.add_field(
                    Conversor.build_field(paragrafo, indicador, descricao)
                )

        # Ensure 001 control field has the correct control number

        for field_001 in record.get_fields('001'):
            record.remove_field(field_001)

        new_001_field = Field(tag='001', data=str(id))
        record.add_ordered_field(new_001_field)

        return record


class PergamumDownloader:
    """Handle the connection to the Pergamum Web Service and transform the
    retrieved data to several representations"""

    def __init__(self) -> None:
        self.base: Dict[str, PergamumWebServiceRequest] = {}

    def _add_base(self, url: str) -> None:
        if url not in self.base:
            self.base[url] = PergamumWebServiceRequest(url)

    def build_record(self, url: str, id: int) -> Record:
        self._add_base(url)
        xml_response = self.base[url].busca_marc(id)
        xml_response = re.sub(r"<br\s?/?>", "", xml_response)
        try:
            dados_marc = DadosMarc(**parse(xml_response)["Dados_marc"])
        except ValidationError:
            raise PergamumWebServiceException(
                "Did not received a valid record. Make sure the id is valid"
            )
        return Conversor.convert_dados_marc_to_record(dados_marc, id)

    def get_marc_iso(self, url: str, id: int) -> BytesIO:
        return BytesIO(self.build_record(url, id).as_marc())

    def get_marc_xml(self, url: str, id: int) -> str:
        return record_to_xml(self.build_record(url, id), namespace=True)
