from fastapi import Header, Request

from packages.errors.errors import UnauthorizedError


def auth_middleware(
    request: Request, authorization: str = Header(...), userEmail: str = Header(None)
):
    """
    This middleware is used to check if the request has a valid token in the header.
    If the token is not valid, it will raise an HTTPException with status code 401.
    Else, it will set the token in the request state.
    """

    if not authorization:
        raise UnauthorizedError(message="Token is missing")
    if not userEmail:
        raise UnauthorizedError(message="User email is missing")

    request.state.token = authorization.split(" ")[1]
    request.state.user_email = userEmail
