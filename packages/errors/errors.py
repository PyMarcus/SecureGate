import json

from packages.encoders.json_encoder import JSONEncoder


class ErrorResponse(Exception):
    def __init__(self, message, status_code, success=False):
        super().__init__(message)
        self.status_code = status_code
        self.success = success

    def dict(self):
        return {"status_code": self.status_code, "success": self.success, "message": str(self)}

    def json(self):
        return json.dumps(self.dict(), cls=JSONEncoder)


class BadRequestError(ErrorResponse):
    def __init__(self, message):
        super().__init__(message, 400)


class NotFoundError(ErrorResponse):
    def __init__(self, message):
        super().__init__(message, 404)


class UnauthorizedError(ErrorResponse):
    def __init__(self, message):
        super().__init__(message, 401)


class ForbiddenError(ErrorResponse):
    def __init__(self, message):
        super().__init__(message, 403)


class InternalServerError(ErrorResponse):
    def __init__(self, message):
        super().__init__(message, 500)
