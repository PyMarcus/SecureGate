from fastapi import Request


def get_request_header(request: Request):
    """
    This function is used to get the request header.
    """
    return {"token": request.state.token, "email": request.state.user_email}
