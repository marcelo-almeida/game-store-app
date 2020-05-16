import logging

from configuration.custom_exception import ApiError
from persistence.platform import Platform, PlatformRepository
from persistence.platform import VALID_CREATE_KEYS, VALID_CREATE_TYPES, VALID_UPDATE_KEYS, VALID_UPDATE_TYPES
from service.validate_platform import validate_request


def create_platform(request: dict) -> dict:
    validate_request(request=request,
                     request_type='create',
                     valid_keys=VALID_CREATE_KEYS,
                     valid_types=VALID_CREATE_TYPES)

    platform = Platform(name=request.get('name'),
                        info=request.get('info')).build_to_create().to_dict()
    repository = PlatformRepository()
    repository.save(platform=platform)
    logging.info('platform created with success.')
    return platform


def update_platform(request: dict) -> dict:
    validate_request(request=request,
                     request_type='update',
                     valid_keys=VALID_UPDATE_KEYS,
                     valid_types=VALID_UPDATE_TYPES)

    repository = PlatformRepository()
    platform_db = repository.get(platform_id=request['platformId'])
    platform = Platform(name=request.get('name'),
                        info=request.get('info'),
                        platform_id=platform_db.platform_id,
                        creation_date=platform_db.creation_date).build_to_update().to_dict()
    repository.save(platform=platform)
    logging.info('platform updated with success.')
    return platform


def get_platform_by_id(platform_id: str) -> dict:
    repository = PlatformRepository()
    platform = repository.get(platform_id=platform_id)
    if platform:
        logging.info('platform retrieved with success.')
        return platform.to_dict()
    else:
        raise ApiError(error_code=404, error_message='platform not found')


def search_platforms(name: str) -> dict:
    repository = PlatformRepository()
    # TODO: implement page.
    return {
        'data': [platform.to_dict() for platform in repository.search(name=name)]
    }
