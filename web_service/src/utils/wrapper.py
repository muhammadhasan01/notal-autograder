from enum import IntEnum
from http import HTTPStatus


def get_response(err: bool, msg: str, data: dict[str, any] = None, status_code: int = HTTPStatus.ACCEPTED):
    return {
        "error": err,
        "message": msg,
        "data": data
    }, status_code
