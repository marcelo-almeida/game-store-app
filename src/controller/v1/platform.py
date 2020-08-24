import logging

from flask import make_response

from configuration.decorators import handler_exception
from service.platform_service import create_platform, update_platform, delete_platform, get_platform_by_id, \
    search_platforms
from service.schema_validator import PlatformSchemaValidator

schema_validator = PlatformSchemaValidator()


@handler_exception
def search(name: str = None):
    logging.info(f'Searching platforms. Param Name: {name}')
    return _create_response(search_platforms(name=name))


@handler_exception
def post(body: dict):
    logging.info('Creating platform.')
    schema_validator.validate_creation_request(request=body)
    return _create_response(response=create_platform(request=body), success_status=201)


@handler_exception
def get(platform_id: str):
    logging.info(f'Getting platform. PlatformId: {platform_id}')
    return _create_response(get_platform_by_id(platform_id=platform_id))


@handler_exception
def put(platform_id: str, body: dict):
    logging.info(f'Updating platform. PlatformId: {platform_id}')
    body['platformId'] = platform_id
    schema_validator.validate_update_request(request=body)
    return _create_response(update_platform(request=body))


@handler_exception
def delete(platform_id: str):
    logging.info(f'Deleting platform. PlatformId: {platform_id}')
    delete_platform(platform_id=platform_id)
    return make_response('', 200)


def _create_response(response: dict, success_status: int = 200):
    return make_response(response, success_status)
