
from io import BytesIO
from requests import Session
from zeep import Client
from zeep.transports import Transport
from pydantic import BaseModel
from typing import Optional
from xmltodict import parse
from pymarc import Record, Field
from pymarc.marcxml import record_to_xml


class DadosMarc(BaseModel):
    """ Represents a Dados_marc object received from Pergamum webservice"""
    paragrafo: list[str]
    indicador: list[Optional[str]]
    descricao: list[Optional[str]]

class Pergamum:

    def __init__(self, base_url: str) -> None:
        session = Session()
        session.headers.update({'Accept-Encoding': 'identity'})
        self.client = Client(
            f'{base_url}/web_service/servidor_ws.php?wsdl', transport=Transport(session=session))

    def busca_marc(self, cod_acervo: int) -> str:
        return self.client.service.busca_marc(codigo_acervo_temp=cod_acervo)


class PergamumDownloader:

    def __init__(self) -> None:
        self.base = {}

    def _add_base(self, url: str) -> None:
        if url not in self.base:
            self.base[url] = Pergamum(url)

    def _convert_to_marc(self, p, i, d):
        # indicators conversion
        # TODO needs improvements
        indicators = [' ', ' ']
        if i:
            i = i.rstrip()
            if len(i.rstrip()) <= 2:
                indicators[0] = i.strip()
            else:
                indicators[1] = i[-1]
                indicators[0] = i[-3]

        # Subfields conversion
        # TODO needs improvements
        subfileds = [s for s in d[1:].split('$')] if d else None
        x = []
        for s in subfileds:
            if s:
                x.append(s[0])
                x.append(s[2:].strip())        
        return Field(
            tag=p.strip(),
            indicators = indicators,
            subfields = x,
            data = d if int(p) < 10 else ''
        )

    def _dados_marc_to_marc(self, dados_marc: DadosMarc) -> Record:
        record = Record(leader='     nam a22      a 4500')

        for paragrafo, indicador, descricao in zip(dados_marc.paragrafo, dados_marc.indicador, dados_marc.descricao):
            if indicador and '<br>' in indicador:
                for indicador, descricao in zip(indicador.split('<br>'), descricao.split('<br>')):
                    record.add_field(self._convert_to_marc(paragrafo, indicador, descricao))
            elif descricao and '<br>' in descricao:
                for descricao in descricao.split('<br>'): 
                    record.add_field(self._convert_to_marc(paragrafo, indicador, descricao))
            else:
                record.add_field(self._convert_to_marc(paragrafo, indicador, descricao))

        return record

    def download_record(self, url: str, id: int) -> Record:
        self._add_base(url)
        dadosmarc_xml = self.base[url].busca_marc(id)
        dados_marc = DadosMarc(**parse(dadosmarc_xml)['Dados_marc'])
        return self._dados_marc_to_marc(dados_marc)

    def download_iso(self, url: str, id: int) -> BytesIO:
        return BytesIO(self.download_record(url, id).as_marc())

    def download_xml(self, url: str, id: int) -> str:
        return record_to_xml(self.download_record(url, id))

