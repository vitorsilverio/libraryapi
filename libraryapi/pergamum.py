import re
import xml.etree.ElementTree as ET
from io import BytesIO
from itertools import chain
from typing import Dict
from typing import List

import pymarc  # type: ignore
import xmltodict
from pydantic import BaseModel
from pydantic.error_wrappers import ValidationError
from pymarc import Field  # type: ignore
from pymarc import Record
from requests import Session  # type: ignore
from requests.exceptions import HTTPError  # type: ignore
from zeep import Client
from zeep.exceptions import XMLSyntaxError
from zeep.transports import Transport


class PergamumWebServiceException(Exception):
    """Represents an exception object in the Pergamum Web Service"""
    def __init__(self, message: str) -> None:
        self.message = message


class DadosMarc(BaseModel):
    """Represents a Dados_marc object received from Pergamum Web Service"""

    paragrafo: List[str]
    indicador: List[str]
    descricao: List[str]


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
        except HTTPError as error:
            raise PergamumWebServiceException(
                message=f"{base_url}/web_service/servidor_ws.php?wsdl returned {error.response.status_code}"
            ) from error
        except XMLSyntaxError:
            raise PergamumWebServiceException(
                "Invalid response from Pergamum WebService."
            )

    def busca_marc(self, cod_acervo: int) -> str:
        """Returns the xml response from the "busca_marc" operation"""
        return self.client.service.busca_marc(codigo_acervo_temp=cod_acervo)


class Conversor:
    """Transform the data retrieved by the Pergamum Web Service "busca_marc"
    request to Pymarc Fields and Records"""

    @staticmethod
    def build_field(paragrafo, indicador, descricao) -> Field:
        """Return Pymarc Field objects in order to build a Pymarc Record"""
        # Indicators handling:
        # Default indicators are "\\" (2 empty spaces).
        # Pergamum WS returns indicators as:
        # - 'X X'
        # - '  X'
        # - 'X  '
        # - 'X X '
        # Logic here consists checking the length of the "indicador" string
        # and then adjusting the values according to their positions.

        indicators = [" ", " "]
        if indicador:
            if len(indicador) == 3:
                indicators[0] = indicador[-3]
                indicators[1] = indicador[-1]
            else:
                indicators[0] = indicador[-4]
                indicators[1] = indicador[-2]

        # Subfields handling:
        # Split the contents at "$", ignoring the first one to avoid the
        # creation of an empty segment. Split them again getting the first
        # position as the subfield code and the rest as the value.

        subfields = (
            list(
                chain.from_iterable(
                    [[subfield[0], subfield[2:]] for subfield in descricao[1:].split("$")]
                )
            )
            if descricao
            else None
        )

        return Field(
            tag=paragrafo.strip(),
            indicators=indicators,
            subfields=subfields,
            data=descricao.replace("#", " ").strip()
            if int(paragrafo) < 10
            else "",  # Only control fields has "data" param
        )

    @staticmethod
    def convert_dados_marc_to_record(dados_marc: DadosMarc, id: int) -> Record:
        """Receive DadosMarc objects and build a Pymarc Record"""
        record = Record(leader="     nam a22      a 4500")

        for paragrafo, indicador, descricao in zip(
            dados_marc.paragrafo, dados_marc.indicador, dados_marc.descricao
        ):
            if not descricao:
                descricao = ""
            if indicador and "<br>" in indicador:
                for indicador, descricao in zip(
                    indicador.split("<br> "), descricao.split(" <br>")
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

        for field_001 in record.get_fields("001"):
            record.remove_field(field_001)

        new_001_field = Field(tag="001", data=str(id))
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
        """Build a Record object from the xml response, validated from
        the DadosMarc model"""
        self._add_base(url)
        xml_response = self.base[url].busca_marc(id)
        xml_response = re.sub(r"<br\s?/?>", "", xml_response)
        xml_response = re.sub(r"&", "&amp;", xml_response)
        xml_response = re.sub(
            r"&amp;lt;br&amp;gt;", "&lt;br&gt;", xml_response
        )
        try:
            dados_marc = DadosMarc(
                **xmltodict.parse(xml_response, strip_whitespace=False)[
                    "Dados_marc"
                ]
            )
        except ValidationError:
            raise PergamumWebServiceException(
                "Did not received a valid record. Make sure the id is valid"
            )
        return Conversor.convert_dados_marc_to_record(dados_marc, id)

    def get_marc_iso(self, url: str, id: int) -> BytesIO:
        """Get the traditional ISO 2709 MARC record format"""
        return BytesIO(self.build_record(url, id).as_marc())

    def get_marc_xml(self, url: str, id: int) -> str:
        """Get the MARCXML format with XML declaration and namespaces"""
        node = pymarc.marcxml.record_to_xml_node(
            self.build_record(url, id), namespace=True
        )
        return ET.tostring(node, encoding="utf-8", xml_declaration=True)
