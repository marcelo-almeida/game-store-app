from flask import abort


class Error(Exception):
    pass


class ApiError(Error):

    def __init__(self, error_code: int = 500, error_message: str = None):
        abort(error_code, description=error_message)
