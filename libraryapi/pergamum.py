
from requests import Session
from zeep import Client
from zeep.transports import Transport
from io import BytesIO
import subprocess

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
        marc_xml = self.base[url].busca_marc(id)
        process = subprocess.run(['saxonb-xslt', '-xsl:pergamumSoap-MarcXML.xsl', '-s:/dev/stdin' ], input=bytes(marc_xml, encoding='utf-8'), capture_output=True)
        process = subprocess.run(['yaz-marcdump', '-i', 'marcxml', '-o', 'marc', '-l', '5=110,9=97,18=97', '/dev/stdin'], input=process.stdout, capture_output = True)
           

        return BytesIO(process.stdout)

    
