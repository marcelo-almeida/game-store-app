import logging

from configuration.custom_exception import ApiError
from persistence.game import Game, GameRepository
from persistence.game import VALID_CREATE_KEYS, VALID_CREATE_TYPES, VALID_UPDATE_KEYS, VALID_UPDATE_TYPES
from service.validate_game import validate_request


def create_game(request: dict) -> dict:
    validate_request(request=request,
                     request_type='create',
                     valid_keys=VALID_CREATE_KEYS,
                     valid_types=VALID_CREATE_TYPES)

    game = Game(account=request.get('account'),
                name=request.get('name'),
                release_date=request.get('releaseDate'),
                price=request.get('price'),
                available_platforms=request.get('availablePlatforms'),
                description=request.get('description')).build_to_create().to_dict()
    repository = GameRepository()
    repository.save(game=game)
    logging.info('game created with success.')
    return game


def update_game(request: dict) -> dict:
    validate_request(request=request,
                     request_type='update',
                     valid_keys=VALID_UPDATE_KEYS,
                     valid_types=VALID_UPDATE_TYPES)

    repository = GameRepository()
    game_db = repository.get(account=request['account'], game_id=request['gameId'])
    game = Game(account=request.get('account'),
                name=request.get('name'),
                release_date=request.get('releaseDate'),
                price=request.get('price'),
                available_platforms=request.get('availablePlatforms'),
                description=request.get('description'),
                game_id=game_db.game_id,
                creation_date=game_db.creation_date).build_to_update().to_dict()
    repository.save(game=game)
    logging.info('game updated with success.')
    return game


def delete_game(account: str, game_id: str):
    repository = GameRepository()
    if repository.get(account=account, game_id=game_id):
        repository.delete(account=account, game_id=game_id)
        logging.info('game deleted with success.')
    else:
        raise ApiError(error_code=404, error_message='game not found')


def get_game_by_id(account: str, game_id: str) -> dict:
    repository = GameRepository()
    game = repository.get(account=account, game_id=game_id)
    if game:
        logging.info('game retrieved with success.')
        return game.to_dict()
    else:
        raise ApiError(error_code=404, error_message='game not found')


def search_games(name: str) -> dict:
    repository = GameRepository()
    # TODO: implement page.
    games = repository.search(name=name)
    logging.info('games retrieved with success.')
    return {
        'data': [game.to_dict() for game in games]
    }
