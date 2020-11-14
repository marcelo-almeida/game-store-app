import logging

from flask import make_response

from configuration.decorators import handler_exception
from service.game_service import create_game, update_game


@handler_exception
def search():
    return 'search game Connexion!'


@handler_exception
def post(body: dict):
    logging.info('Creating game.')
    return __create_response(response=create_game(request=body), success_status=201)


@handler_exception
def get(game_id: str):
    return 'get game Connexion! {}'.format(game_id)


@handler_exception
def put(game_id: str, body: dict):
    logging.info(f'Updating game. GameId:{game_id}')
    body['gameId'] = game_id
    return __create_response(response=update_game(request=body), success_status=200)


@handler_exception
def delete(game_id: str):
    return 'delete game Connexion! {}'.format(game_id)


def __create_response(response: dict, success_status: int = 200):
    return make_response(response, success_status)
