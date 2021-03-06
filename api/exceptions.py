from itsdangerous import BadData
from marshmallow import ValidationError
from werkzeug.datastructures import WWWAuthenticate

from .result import ApiResult


class ApiException(Exception):
    def __init__(self, message, status=400, headers=None):
        self.message = message
        self.status = status
        self.headers = headers

    def to_result(self):
        body = {"status": self.status}
        if self.message:
            body["message"] = self.message
        return ApiResult(body, status=self.status, headers=self.headers)


class AuthException(ApiException):
    def __init__(self, error=None, status=401, headers=None):
        www_auth_header = WWWAuthenticate(auth_type="Bearer")
        www_auth_header["realm"] = "api.districtr.org"

        if error is not None:
            www_auth_header["error"] = error

        if headers is None:
            headers = dict()
        headers["WWW-Authenticate"] = www_auth_header.to_header()

        super().__init__(None, status, headers)


class Unauthenticated(AuthException):
    def __init__(self):
        super().__init__(status=401)


class Unauthorized(AuthException):
    def __init__(self):
        super().__init__(error="insufficient_scope", status=403)


class InvalidToken(AuthException):
    def __init__(self):
        super().__init__(error="invalid_token", status=401)


def not_found(error):
    return ApiException("Resource not found.", 404).to_result()


def convert_validation_error_to_api_result(error):
    return ApiResult(
        {
            "status": 400,
            "message": "The provided data did not conform to the proper schema.",
            "errors": error.normalized_messages(),
        },
        status=400,
    )


def register_error_handlers(app):
    app.register_error_handler(ApiException, lambda err: err.to_result())
    app.register_error_handler(404, not_found)
    app.register_error_handler(BadData, lambda err: InvalidToken().to_result())
    app.register_error_handler(ValidationError, convert_validation_error_to_api_result)
