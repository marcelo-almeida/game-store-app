import logging
from persistence.game import GameRepository
from configuration.custom_exception import ApiError


def _is_type_valid(value, value_type) -> bool:
    return isinstance(value, value_type)


def validate_request(request: dict, request_type: str, valid_keys: list, valid_types: dict):
    logging.info(f'validating {request_type} request.')
    if not request:
        raise ApiError(error_code=400, error_message='Invalid Body.')
    else:
        for key, value in request.items():
            if key not in valid_keys:
                raise ApiError(error_code=400, error_message=f'Invalid parameter {key}.')
            elif not _is_type_valid(value=value, value_type=valid_types[key]):
                raise ApiError(error_code=400, error_message=f'Invalid value for parameter {key}.')

        if 'account' not in request or not request['account'] or len(request['account']) <= 0:
            raise ApiError(error_code=400, error_message=f'Account is a required parameter.')

        if 'name' not in request or not request['name'] or len(request['name']) <= 0:
            raise ApiError(error_code=400, error_message=f'Name is a required parameter.')

        if 'releaseDate' not in request or not request['releaseDate'] or len(request['releaseDate']) <= 0:
            raise ApiError(error_code=400, error_message=f'Release Date is a required parameter.')

        if 'price' not in request or not request['price'] or request['name'] < 0:
            raise ApiError(error_code=400, error_message=f'Price is a required parameter.')

        # TODO: validate platforms if exists.

        repository = GameRepository()
        games = repository.search(name=request['name'], validate=True)
        if 'update' == request_type:
            if not repository.get(account=request['account'], game_id=request['gameId']):
                    raise ApiError(error_code=404, error_message=f'Game does not exists to be updated.')
            if 'gameId' not in request or not request['gameId'] or len(request['gameId']) <= 0:
                    raise ApiError(error_code=400, error_message=f'GameId is a required parameter.')
            if len(games) > 0 and games[0].game_id != request['gameId']:
                    raise ApiError(error_code=409, error_message=f'The given name is being used.')
        else:
            if len(games) > 0:
                raise ApiError(error_code=409, error_message=f'The given name is being used.')
