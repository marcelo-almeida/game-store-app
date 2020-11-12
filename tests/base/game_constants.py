GAME_CREATE_PAYLOAD = {
    'account': 'store-1',
    'name': 'game_name 测试',
    'description': 'a small description 测试',
    'releaseDate': '05-27-2020',
    'price': '39.90',
    'availablePlatforms': [{'id': '1'}]
}

GAME_UPDATE_PAYLOAD = {**GAME_CREATE_PAYLOAD, 'gameId': '1'}
INVALID_GAME_PAYLOAD = {**GAME_CREATE_PAYLOAD}
del INVALID_GAME_PAYLOAD['name']
