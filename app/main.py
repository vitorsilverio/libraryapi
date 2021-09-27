from fastapi import FastAPI
from fastapi.responses import Response
from fastapi.responses import StreamingResponse

from libraryapi.pergamum import PergamumDownloader


app = FastAPI()
pergamumDownloader = PergamumDownloader()


@app.get("/get_marc")
async def get_marc(url: str, id: int) -> StreamingResponse:
    response = StreamingResponse(
        pergamumDownloader.download_iso(url, id), media_type="application/marc"
    )
    response.headers["Content-Disposition"] = f"attachment; filename={id}.mrc"
    return response


@app.get("/get_marcxml")
async def get_marcxml(url: str, id: int) -> Response:
    response = Response(
        pergamumDownloader.download_xml(url, id), media_type="application/xml"
    )
    response.headers["Content-Disposition"] = f"attachment; filename={id}.xml"
    return response
