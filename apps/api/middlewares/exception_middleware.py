from fastapi import Request
from fastapi.exceptions import HTTPException
from starlette.responses import JSONResponse

from packages.errors.errors import ErrorResponse


def exception_middleware(request: Request, exc: Exception) -> JSONResponse | HTTPException:
    if isinstance(exc, ErrorResponse):
        error_response = exc.dict()
        status_code = error_response.get("status_code", 500)
        return JSONResponse(content=error_response, status_code=status_code)
    elif isinstance(exc, HTTPException):
        return exc
