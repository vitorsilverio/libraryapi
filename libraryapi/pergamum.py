
from requests import Session
from zeep import Client
from zeep.transports import Transport
from libraryapi.util import new_temp_xml
from io import BytesIO
import subprocess
import os

class Pergamum:

    def __init__(self, base_url: str) -> None:
        session = Session()
        session.headers.update({'Accept-Encoding': 'identity'})
        self.client = Client(f'{base_url}/web_service/servidor_ws.php?wsdl', transport=Transport(session=session))

    def busca_marc(self, cod_acervo: int) -> str:
        return self.client.service.busca_marc(codigo_acervo_temp=cod_acervo)

class PergamumDownloader:

    def __init__(self) -> None:
        self.base = {}

    def _add_base(self, url: str) -> None:
        if url not in self.base:
            self.base[url] = Pergamum(url)

    def download_iso(self, url: str, id: int):
        self._add_base(url)

        dados_marc_xml = new_temp_xml(bytes(self.base[url].busca_marc(id), encoding='utf-8'))
        process = subprocess.run(['saxonb-xslt', '-xsl:/pergamumSoap-MarcXML.xsl', f'-s:{dados_marc_xml}' ], capture_output=True)
        process = subprocess.run(['yaz-marcdump', '-i', 'marcxml', '-o', 'marc', '-l', '5=110,9=97,18=97', '/dev/stdin'], input=process.stdout, capture_output = True)
        os.unlink(dados_marc_xml)      

        return BytesIO(process.stdout)

    
