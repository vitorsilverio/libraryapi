from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse

from libraryapi.pergamum import PergamumWebServiceException


def configure(app: FastAPI) -> None:
    @app.exception_handler(PergamumWebServiceException)
    async def pergamum_handle(request: Request, exc: PergamumWebServiceException):
        return JSONResponse(
            status_code=400,
            content={
                "code": 400,
                "error": "BAD REQUEST",
                "message": exc.message,
            },
        )
