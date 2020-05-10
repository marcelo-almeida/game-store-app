from persistence.platform import Platform, PlatformRepository
from persistence.platform import VALID_CREATE_KEYS, VALID_CREATE_TYPES, VALID_UPDATE_KEYS, VALID_UPDATE_TYPES
from service.validate_platform import validate_request


def create_platform(request: dict) -> dict:
    validator = validate_request(request=request,
                                 request_type='create',
                                 valid_keys=VALID_CREATE_KEYS,
                                 valid_types=VALID_CREATE_TYPES)
    if 'error' not in validator:
        platform = Platform(name=request.get('name'),
                            subtype=request.get('subtype')).build_to_create().to_dict()
        repository = PlatformRepository()
        repository.save(platform=platform)
        return platform
    else:
        return validator


def update_platform(request: dict) -> dict:
    validator = validate_request(request=request,
                                 request_type='update',
                                 valid_keys=VALID_UPDATE_KEYS,
                                 valid_types=VALID_UPDATE_TYPES)
    if 'error' not in validator:
        repository = PlatformRepository()
        platform_db = repository.get(platform_id=request['platformId'])
        platform = Platform(name=request.get('name'),
                            subtype=request.get('subtype'),
                            platform_id=platform_db.platform_id,
                            creation_date=platform_db.creation_date).build_to_update().to_dict()
        repository.save(platform=platform)
        return platform
    else:
        return validator
