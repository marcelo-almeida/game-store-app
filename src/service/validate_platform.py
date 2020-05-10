import logging
from persistence.platform import PlatformRepository


def _is_type_valid(value, value_type) -> bool:
    return isinstance(value, value_type)


def validate_request(request: dict, request_type: str, valid_keys: list, valid_types: dict) -> dict:
    logging.info(f'validating {request_type} request.')
    request_validated = {}
    if not request:
        request_validated['error'] = 'Invalid Body.'
    else:
        for key, value in request.items():
            if key not in valid_keys:
                request_validated['error'] = f'Invalid parameter {key}.'
                break
            elif not _is_type_valid(value=value, value_type=valid_types[key]):
                request_validated['error'] = f'Invalid value for parameter {key}.'
                break

        if 'name' not in request or not request['name'] or len(request['name']) <= 0:
            request_validated['error'] = f'Name is a required parameter.'

        if 'error' not in request_validated:
            repository = PlatformRepository()
            platforms = repository.search(name=request['name'], validate=True)
            if 'update' == request_type:
                if 'platformId' not in request or not request['platformId'] or len(request['platformId']) <= 0:
                    request_validated['error'] = f'PlatformId is a required parameter.'

                if len(platforms) > 0 and platforms[0]['platformId'] != request['platformId']:
                    request_validated['error'] = f'The given name is being used.'
                if not repository.get(platform_id=request['platformId']):
                    # TODO: may create a new status code for this one.
                    request_validated['error'] = f'Platform does not exists to be updated.'
            else:
                if len(platforms) > 0:
                    request_validated['error'] = f'The given name is being used.'
    return request_validated
