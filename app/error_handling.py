# Error handling basics
# Error part 2: try/ except/ else/ finally demonstration

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

def add_exception_handlers(app: FastAPI):
    """Add custom exception handlers to FastAPI app"""
    
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request, exc):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "detail": exc.errors(),
                "body": exc.body
            }
        )
    
    @app.exception_handler(ValidationError)
    async def pydantic_validation_handler(request, exc):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": exc.errors()}
        )