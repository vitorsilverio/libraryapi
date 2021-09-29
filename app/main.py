from fastapi import FastAPI
from fastapi.responses import Response
from fastapi.responses import StreamingResponse

from app.util import attach_file
from libraryapi.pergamum import PergamumDownloader


app = FastAPI()
pergamumDownloader = PergamumDownloader()


@app.get("/pergamum/get_marc")
async def get_marc_iso(url: str, id: int) -> StreamingResponse:
    response = StreamingResponse(
        pergamumDownloader.get_marc_iso(url, id), media_type="application/marc"
    )
    attach_file(response, id, "mrc")
    return response


@app.get("/pergamum/get_marcxml")
async def get_marc_xml(url: str, id: int) -> Response:
    response = Response(
        pergamumDownloader.get_marc_xml(url, id), media_type="application/xml"
    )
    return response
