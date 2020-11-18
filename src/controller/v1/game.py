import logging

from flask import make_response

from configuration.decorators import handler_exception
from service.game_service import create_game, update_game, get_game_by_id, search_games, delete_game


@handler_exception
def search(name: str = None):
    logging.info('Searching games.')
    return __create_response(response=search_games(name=name), success_status=200)


@handler_exception
def post(body: dict):
    logging.info('Creating game.')
    return __create_response(response=create_game(request=body), success_status=201)


@handler_exception
def get(account: str, game_id: str):
    return __create_response(response=get_game_by_id(account=account, game_id=game_id))


@handler_exception
def put(account: str, game_id: str, body: dict):
    logging.info(f'Updating game. GameId:{game_id}')
    body['gameId'] = game_id
    body['account'] = account
    return __create_response(response=update_game(request=body), success_status=200)


@handler_exception
def delete(account: str, game_id: str):
    logging.info('Deleting game.')
    delete_game(account=account, game_id=game_id)
    return __create_response(response={}, success_status=200)


def __create_response(response: dict, success_status: int = 200):
    return make_response(response, success_status)
