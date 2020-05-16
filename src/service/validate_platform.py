import logging
from persistence.platform import PlatformRepository
from configuration.custom_exception import ApiError


def _is_type_valid(value, value_type) -> bool:
    return isinstance(value, value_type)


def validate_request(request: dict, request_type: str, valid_keys: list, valid_types: dict):
    logging.info(f'validating {request_type} request.')
    request_validated = {}
    if not request:
        raise ApiError(error_code=400, error_message='Invalid Body.')
    else:
        for key, value in request.items():
            if key not in valid_keys:
                raise ApiError(error_code=400, error_message=f'Invalid parameter {key}.')
            elif not _is_type_valid(value=value, value_type=valid_types[key]):
                raise ApiError(error_code=400, error_message=f'Invalid value for parameter {key}.')

        if 'name' not in request or not request['name'] or len(request['name']) <= 0:
            raise ApiError(error_code=400, error_message=f'Name is a required parameter.')

        if 'error' not in request_validated:
            repository = PlatformRepository()
            platforms = repository.search(name=request['name'], validate=True)
            if 'update' == request_type:
                if not repository.get(platform_id=request['platformId']):
                    raise ApiError(error_code=404, error_message=f'Platform does not exists to be updated.')
                if 'platformId' not in request or not request['platformId'] or len(request['platformId']) <= 0:
                    raise ApiError(error_code=400, error_message=f'PlatformId is a required parameter.')
                if len(platforms) > 0 and platforms[0].platform_id != request['platformId']:
                    raise ApiError(error_code=409, error_message=f'The given name is being used.')
            else:
                if len(platforms) > 0:
                    raise ApiError(error_code=409, error_message=f'The given name is being used.')
