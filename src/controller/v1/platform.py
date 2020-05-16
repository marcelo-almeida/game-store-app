import logging

from flask import make_response

from service.platform_service import create_platform, update_platform, get_platform_by_id


def search():
    return 'search platform Connexion!'


def post(body: dict):
    logging.info('Creating platform.')
    return _create_response(response=create_platform(request=body), success_status=201)


def get(platform_id: str):
    logging.info(f'Getting platform. PlatformId: {platform_id}')
    return _create_response(get_platform_by_id(platform_id=platform_id))


def put(platform_id: str, body: dict):
    logging.info(f'Updating platform. PlatformId: {platform_id}')
    body['platformId'] = platform_id
    return _create_response(update_platform(request=body))


def delete(platform_id: str):
    return 'delete platform Connexion! {}'.format(platform_id)


def _create_response(response: dict, success_status: int = 200):
    return make_response(response, success_status)
