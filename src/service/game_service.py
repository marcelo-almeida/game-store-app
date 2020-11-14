import logging

from configuration.custom_exception import ApiError
from service.game import Game, GameRepository
from service.platform import PlatformRepository
from service.schema_validator import GameSchemaValidator

repository = GameRepository()
platform_repository = PlatformRepository()
schema_validator = GameSchemaValidator()


def create_game(request: dict) -> dict:
    schema_validator.validate_creation_request(request=request)
    validate_game(request=request)
    platforms = fill_platforms(platform_ids=[item.get('id') for item in request.get('availablePlatforms')])
    game = Game(account=request.get('account'),
                name=request.get('name'),
                release_date=request.get('releaseDate'),
                price=request.get('price'),
                available_platforms=platforms,
                description=request.get('description')).build_to_create().to_dict()
    repository.save(game=game)
    logging.info('game created with success.')
    return game


def update_game(request: dict) -> dict:
    schema_validator.validate_update_request(request=request)
    validate_game(request=request)
    platforms = fill_platforms(platform_ids=[item.get('id') for item in request.get('availablePlatforms')])
    game_db = repository.get(account=request['account'], game_id=request['gameId'])
    game = Game(account=request.get('account'),
                name=request.get('name'),
                release_date=request.get('releaseDate'),
                price=request.get('price'),
                available_platforms=platforms,
                description=request.get('description'),
                game_id=game_db.game_id,
                creation_date=game_db.creation_date).build_to_update().to_dict()
    repository.save(game=game)
    logging.info('game updated with success.')
    return game


def delete_game(account: str, game_id: str):
    if repository.get(account=account, game_id=game_id):
        repository.delete(account=account, game_id=game_id)
        logging.info('game deleted with success.')
    else:
        raise ApiError(error_code=404, error_message='game not found')


def get_game_by_id(account: str, game_id: str) -> dict:
    game = repository.get(account=account, game_id=game_id)
    if game:
        logging.info('game retrieved with success.')
        return game.to_dict()
    else:
        raise ApiError(error_code=404, error_message='game not found')


def search_games(name: str) -> dict:
    # TODO: implement page.
    games = repository.search(name=name)
    logging.info('games retrieved with success.')
    return {
        'data': [game.to_dict() for game in games]
    }


def fill_platforms(platform_ids: list):
    platforms = []
    for platform in platform_ids:
        platforms.append(platform_repository.get(platform_id=platform).to_dict())
    return platforms


def validate_platforms(platform_ids: list):
    platforms_ddb = [item.platform_id for item in platform_repository.search()]
    if not set(platform_ids).issubset(set(platforms_ddb)):
        raise ApiError(error_code=404, error_message='One or more platforms are invalid.')


def validate_game(request: dict):
    games = repository.search(name=request['name'], account=request['account'], validate=True)
    if request.get('gameId'):
        if len(games) > 0 and games[0].game_id != request['gameId']:
            raise ApiError(error_code=409, error_message='The given name is being used.')
        if not repository.get(account=request['account'], game_id=request['gameId']):
            raise ApiError(error_code=404, error_message='Game does not exists to be updated.')
    else:
        if len(games) > 0:
            raise ApiError(error_code=409, error_message=f'The given name is being used.')
    validate_platforms(platform_ids=[item.get('id') for item in request['availablePlatforms']])
