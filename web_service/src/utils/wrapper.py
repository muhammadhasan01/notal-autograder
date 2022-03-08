def get_response(err: bool, msg: str, data: dict[str, any] = None, status_code: int = 200):
    return {
        "error": err,
        "message": msg,
        "data": data
    }, status_code
