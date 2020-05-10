from persistence.platform import Platform
from persistence.platform import VALID_CREATE_KEYS, VALID_CREATE_TYPES
from service.validate_platform import validate_request


def create_platform(request: dict) -> dict:
    validator = validate_request(request=request,
                                 request_type='create',
                                 valid_keys=VALID_CREATE_KEYS,
                                 valid_types=VALID_CREATE_TYPES)
    if 'error' not in validator:
        platform = Platform(request=request).to_dict()
        # TODO: save item
        return platform
    else:
        return validator


def update_platform(request: dict) -> dict:
    return request
