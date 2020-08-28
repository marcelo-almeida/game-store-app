import logging

from configuration.custom_exception import ApiError
from service.platform import Platform, PlatformRepository

repository = PlatformRepository()


def create_platform(request: dict) -> dict:
    validate_platform(request=request)
    platform = Platform(name=request.get('name'),
                        info=request.get('info')).build_to_create().to_dict()
    repository.save(platform=platform)
    logging.info('platform created with success.')
    return platform


def update_platform(request: dict) -> dict:
    validate_platform(request=request)
    platform_db = repository.get(platform_id=request.get('platformId'))
    platform = Platform(name=request.get('name'),
                        info=request.get('info'),
                        platform_id=platform_db.platform_id,
                        creation_date=platform_db.creation_date).build_to_update().to_dict()
    repository.save(platform=platform)
    logging.info('platform updated with success.')
    return platform


def delete_platform(platform_id: str):
    if repository.get(platform_id=platform_id):
        repository.delete(platform_id=platform_id)
        logging.info('platform deleted with success.')
    else:
        raise ApiError(error_code=404, error_message='platform not found')


def get_platform_by_id(platform_id: str) -> dict:
    platform = repository.get(platform_id=platform_id)
    if platform:
        logging.info('platform retrieved with success.')
        return platform.to_dict()
    else:
        raise ApiError(error_code=404, error_message='platform not found')


def search_platforms(name: str) -> dict:
    # TODO: implement page.
    platforms = repository.search(name=name)
    logging.info('platforms retrieved with success.')
    return {
        'data': [platform.to_dict() for platform in platforms]
    }


def validate_platform(request: dict):
    platforms = repository.search(name=request['name'], validate=True)
    if request.get('platformId'):
        if len(platforms) > 0 and platforms[0].platform_id != request['platformId']:
            raise ApiError(error_code=409, error_message=f'The given name is being used.')
        if not repository.get(platform_id=request['platformId']):
            raise ApiError(error_code=404, error_message=f'Platform does not exists to be updated.')
    else:
        if len(platforms) > 0:
            raise ApiError(error_code=409, error_message=f'The given name is being used.')
