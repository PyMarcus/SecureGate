from fastapi import Header, HTTPException, Request


def auth_middleware(request: Request, authorization: str = Header(...)):
    """
    This middleware is used to check if the request has a valid token in the header.
    If the token is not valid, it will raise an HTTPException with status code 401.
    Else, it will set the token in the request state.
    """

    if authorization is None:
        raise HTTPException(status_code=401, detail="Authorization header is missing")
    request.state.token = authorization


# set dependencies=[Depends(auth_middleware)] in route method
# set request: Request as param in route method
# set request.state.token as param in route method
