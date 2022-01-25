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
    return await get_pergamum_record(
        id, url=url, mime_format="application/marc"
    )


@app.get("/pergamum/xml")
async def get_marc_xml(url: str, id: int) -> Response:
    return await get_pergamum_record(
        id, url=url, mime_format="application/xml"
    )


@app.get("/pergamum/mrk")
async def get_marc_mrk(url: str, id: int) -> Response:
    return await get_pergamum_record(id, url=url, mime_format="text/plain")


@app.get("/api/v2/pergamum/{id}")
async def get_pergamum_record(
    id: int,
    server: str
    | None = Header(
        default=None,
        description="Pergamum Server URI to get data to transform",
        example="https://pergamum.ufsc.br/pergamum/web_service/servidor_ws.php",
    ),
    accept: str = Header(
        default=None,
        description="MIME type required. Available formats are "
        + "(application/marc, application/xml, text/plain)",
    ),
    url: str
    | None = Query(
        default=None,
        description="Pergamum Server URI to get data to transform",
        example="https://pergamum.ufsc.br/pergamum/web_service/servidor_ws.php",
    ),
    mime_format: str
    | None = Query(
        default=None,
        description="MIME type required. Available formats are "
        + "(application/marc, application/xml, text/plain)",
        example="application/marc",
    ),
) -> Response:
    if url:
        server = url
    if mime_format:
        accept = mime_format
    if server:
        record = pergamumDownloader.build_record(server, id)
        response = util.metadata_provider.get(accept, util.marc_provider)(
            record
        )
        return response
    return Response(
        "Neither server Header nor URL query param specified",
        status_code=400,
    )
