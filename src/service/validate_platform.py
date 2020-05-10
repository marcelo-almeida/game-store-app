import logging


def _is_type_valid(value, value_type) -> bool:
    return isinstance(value, value_type)


def validate_request(request: dict, request_type: str, valid_keys: list, valid_types: dict):
    # TODO: validate unique name.
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
    return request_validated
