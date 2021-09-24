from fastapi import FastAPI
from libraryapi.pergamum import PergamumDownloader
from fastapi.responses import StreamingResponse

app = FastAPI()
pergamumDownloader = PergamumDownloader()

@app.get("/download_pergamum_marciso")
async def download_pergamum_marciso(url: str, id: int):
    return StreamingResponse(pergamumDownloader.download_iso(url, id), media_type="application/marc")