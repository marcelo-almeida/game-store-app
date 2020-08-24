import logging

from werkzeug.exceptions import HTTPException

from configuration.custom_exception import ApiError


def handler_exception(func):
    def wrapper(*args, **kwargs):
        try:
            response = func(*args, **kwargs)
        except HTTPException as http_exception:
            raise http_exception
        except Exception as ex:
            logging.error(ex)
            raise ApiError()
        return response

    return wrapper
