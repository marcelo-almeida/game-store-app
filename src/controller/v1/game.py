from service.schema_validator import PlatformSchemaValidator

schema_validator = PlatformSchemaValidator()


def search():
    return 'search game Connexion!'


def post(body: dict):
    schema_validator.validate_creation_request(request=body)
    return 'post game Connexion!'


def get(game_id: str):
    return 'get game Connexion! {}'.format(game_id)


def put(game_id: str, body: dict):
    schema_validator.validate_update_request(request=body)
    return 'put game Connexion! {}'.format(game_id)


def delete(game_id: str):
    return 'delete game Connexion! {}'.format(game_id)
