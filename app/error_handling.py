# Error handling basics
# Error part 2: try/ except/ else/ finally demonstration

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError


def add_exception_handlers(app: FastAPI):

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request, exc):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "detail": [
                    {
                        "field": e.get("loc", [])[-1] if e.get("loc") else "unknown",
                        "message": e.get("msg", "Validation error"),
                        "type": e.get("type", "unknown"),
                    }
                    for e in exc.errors()
                ]
            }
        )

    @app.exception_handler(ValidationError)
    async def pydantic_validation_handler(request, exc):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "detail": [
                    {
                        "field": e.get("loc", [])[-1] if e.get("loc") else "unknown",
                        "message": e.get("msg", "Validation error"),
                        "type": e.get("type", "unknown"),
                    }
                    for e in exc.errors()
                ]
            }
        )