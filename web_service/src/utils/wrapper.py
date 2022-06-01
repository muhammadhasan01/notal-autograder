from enum import IntEnum
from http import HTTPStatus


def get_response(err: bool, msg: str, data: dict[str, any] = None, status_code: int = HTTPStatus.ACCEPTED):
    ret = {
        "error": err,
        "message": msg
    }
    if data:
        ret["data"] = data
    return ret, status_code
