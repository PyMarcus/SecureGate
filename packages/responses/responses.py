import json

from packages.encoders.json_encoder import JSONEncoder


class SuccessResponse:
    def __init__(self, message, data=None, status_code=200, success=True):
        self.message = message
        self.data = data
        self.status_code = status_code
        self.success = success

    def dict(self):
        return self.__dict__

    def json(self):
        return json.dumps(self.dict(), cls=JSONEncoder)


class OKResponse(SuccessResponse):
    def __init__(self, message=None, data=None):
        super().__init__(message, data, 200)


class CreatedResponse(SuccessResponse):
    def __init__(self, message=None, data=None):
        super().__init__(message, data, 201)


class NoContentResponse(SuccessResponse):
    def __init__(self, message=None, data=None):
        super().__init__(message, data, 204)


class ServerErrorResponse(SuccessResponse):
    def __init__(self, message=None, data=None):
        super().__init__(message, data, 500)
