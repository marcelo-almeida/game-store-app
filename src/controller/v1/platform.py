import logging

from flask import make_response, abort

from service.platform_service import create_platform, update_platform


def search():
    return 'search platform Connexion!'


def post(body: dict):
    logging.info('Creating platform.')
    return _create_response(response=create_platform(request=body), success_status=201)


def get(platform_id: str):
    return 'get platform Connexion! {}'.format(platform_id)


def put(platform_id: str, body: dict):
    logging.info(f'Updating platform. PlatformId: {platform_id}')
    body['platformId'] = platform_id
    return _create_response(update_platform(request=body))


def delete(platform_id: str):
    return 'delete platform Connexion! {}'.format(platform_id)


def _create_response(response: dict, success_status: int = 200):
    if 'error' in response:
        abort(400, response['error'])
    else:
        return make_response(response, success_status)
