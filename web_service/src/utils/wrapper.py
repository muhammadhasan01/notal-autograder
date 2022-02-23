def get_response(err: bool, msg: str, additional: dict[str, any] = None, status_code: int = 200):
    ret = {
        "error": err,
        "message": msg
    }
    if additional:
        for key, item in additional.items():
            ret[key] = item
    return ret, status_code
