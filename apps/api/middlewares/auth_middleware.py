from fastapi import Header, HTTPException, Request


def auth_middleware(
    request: Request, authorization: str = Header(...), userEmail: str = Header(None)
):
    """
    This middleware is used to check if the request has a valid token in the header.
    If the token is not valid, it will raise an HTTPException with status code 401.
    Else, it will set the token in the request state.
    """

    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header is missing")
    if not userEmail:
        raise HTTPException(status_code=401, detail="userId header is missing")

    request.state.token = authorization
    request.state.user_email = userEmail
