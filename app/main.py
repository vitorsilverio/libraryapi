from fastapi import FastAPI
from fastapi import Header
from fastapi import Query
from fastapi.responses import Response

import app.error as error
import app.util as util
from libraryapi.pergamum import PergamumDownloader


app = FastAPI()
pergamumDownloader = PergamumDownloader()
error.configure(app)


@app.get("/pergamum/mrc")
async def get_marc_iso(url: str, id: int) -> Response:
    return await get_pergamum_record(id, url=url, media_type="application/marc")


@app.get("/pergamum/xml")
async def get_marc_xml(url: str, id: int) -> Response:
    return await get_pergamum_record(id, url=url, media_type="application/xml")


@app.get("/pergamum/mrk")
async def get_marc_mrk(url: str, id: int) -> Response:
    return await get_pergamum_record(id, url=url, media_type="text/plain")


@app.get("/api/v2/pergamum/{id}")
async def get_pergamum_record(
    id: int,
    server: str | None = Header(
        default=None,
        description="Pergamum Web Service URI",
        examples="https://pergamum.ufsc.br/pergamum/web_service/servidor_ws.php",
    ),
    accept: str = Header(
        default=None,
        description="Media type required. Available options are "
        + "(application/marc, application/xml, text/plain, application/json)",
    ),
    url: str | None = Query(
        default=None,
        description="Pergamum Web Service URI",
        examples="https://pergamum.ufsc.br/pergamum/web_service/servidor_ws.php",
    ),
    media_type: str | None = Query(
        default=None,
        description="Media type required. Available options are "
        + "(application/marc, application/xml, text/plain, application/json)",
        examples="application/marc",
    ),
) -> Response:
    if url:
        server = url
    if media_type:
        accept = media_type
    if server:
        record = await pergamumDownloader.build_record(server, id)
        response = util.media_types.get(accept, util.json_provider)(record)
        return response
    return Response(
        "Neither the server Header nor the URL query param was specified",
        status_code=400,
    )
