from io import BytesIO
from itertools import chain
from typing import Optional

from pydantic import BaseModel
from pymarc import Field
from pymarc import Record
from pymarc.marcxml import record_to_xml
from requests import Session
from xmltodict import parse
from zeep import Client
from zeep.transports import Transport


class DadosMarc(BaseModel):
    """Represents a Dados_marc object received from Pergamum webservice"""

    paragrafo: list[str]
    indicador: list[Optional[str]]
    descricao: list[Optional[str]]


class Pergamum:
    def __init__(self, base_url: str) -> None:
        session = Session()
        session.headers.update({"Accept-Encoding": "identity"})
        self.client = Client(
            f"{base_url}/web_service/servidor_ws.php?wsdl",
            transport=Transport(session=session),
        )

    def busca_marc(self, cod_acervo: int) -> str:
        return self.client.service.busca_marc(codigo_acervo_temp=cod_acervo)


class Conversor:
    @staticmethod
    def build_field(paragrafo, indicador, descricao) -> Field:
        # indicators conversion
        """
        Default indicators are "\\" (2 empry spaces)
        Pergamum returns indicators as:
        - ' X X '
        - 'X X '
        - 'X X'
        and more.
        Logic here consists remove trailing space and get last char as second
        indicator and last -2 as first indicator
        """
        indicators = [" ", " "]
        if indicador:
            indicador = indicador.rstrip()
            if len(indicador.rstrip()) <= 2:
                indicators[0] = indicador.strip()
            else:
                indicators[0] = indicador[-3]
                indicators[1] = indicador[-1]

        # Subfields conversion
        """
        Split subfields at $, but ignore fist one $ to avoid create
        a empty one. Split again getting first position to code and
        third one at least for value
        """
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
            data=descricao
            if int(paragrafo) < 10
            else "",  # Only control fields has data
        )

    @staticmethod
    def convert_dados_marc_to_record(dados_marc: DadosMarc) -> Record:
        record = Record(leader="     nam a22      a 4500")

        for paragrafo, indicador, descricao in zip(
            dados_marc.paragrafo, dados_marc.indicador, dados_marc.descricao
        ):
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

        return record


class PergamumDownloader:
    def __init__(self) -> None:
        self.base = {}

    def _add_base(self, url: str) -> None:
        if url not in self.base:
            self.base[url] = Pergamum(url)

    def download_record(self, url: str, id: int) -> Record:
        self._add_base(url)
        dadosmarc_xml = self.base[url].busca_marc(id)
        dados_marc = DadosMarc(**parse(dadosmarc_xml)["Dados_marc"])
        return Conversor.convert_dados_marc_to_record(dados_marc)

    def download_iso(self, url: str, id: int) -> BytesIO:
        return BytesIO(self.download_record(url, id).as_marc())

    def download_xml(self, url: str, id: int) -> str:
        return record_to_xml(self.download_record(url, id), namespace=True)
