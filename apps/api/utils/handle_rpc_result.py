from fastapi.responses import JSONResponse

from packages.errors.errors import ErrorResponse, InternalServerError


def handle_rpc_result(result):
    try:
        if result.get("success", False):
            return result
        error_response = ErrorResponse(**result)
        status_code = error_response.status_code
        return JSONResponse(content=error_response.dict(), status_code=status_code)
    except Exception as e:
        raise InternalServerError(str(e))
