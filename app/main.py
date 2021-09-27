from fastapi import FastAPI
from fastapi.responses import Response
from fastapi.responses import StreamingResponse

from app.util import attach_file
from libraryapi.pergamum import PergamumDownloader


app = FastAPI()
pergamumDownloader = PergamumDownloader()


@app.get("/get_marc")
async def get_marc(url: str, id: int) -> StreamingResponse:
    response = StreamingResponse(
        pergamumDownloader.download_iso(url, id), media_type="application/marc"
    )
    attach_file(response, id, "mrc")
    return response


@app.get("/get_marcxml")
async def get_marcxml(url: str, id: int) -> Response:
    response = Response(
        pergamumDownloader.download_xml(url, id), media_type="application/xml"
    )
    attach_file(response, id, "xml")
    return response
