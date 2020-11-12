from schema import Schema, SchemaError, And, Optional

from configuration.custom_exception import ApiError

PLATFORM_CREATION_SCHEMA = {
    'name': And(str, lambda s: len(s) > 0, error='Invalid value for parameter name'),
    Optional('info'): And(str, error='Invalid value for parameter info')
}

PLATFORM_UPDATE_SCHEMA = {
    'platformId': And(str, lambda s: len(s) > 0, error='Invalid value for parameter platformId'),
    **PLATFORM_CREATION_SCHEMA
}

GAME_CREATION_SCHEMA = {
    'account': And(str, lambda s: len(s) > 0, error='Invalid value for parameter account'),
    'name': And(str, lambda s: len(s) > 0, error='Invalid value for parameter name'),
    Optional('description'): And(str, lambda s: len(s) > 0, error='Invalid value for parameter description'),
    'releaseDate': And(str, lambda s: len(s) > 0, error='Invalid value for parameter releaseDate'),
    'price': And(str, lambda f: len(f) > 0, error='Invalid value for parameter price'),
    'availablePlatforms': And([{'id': And(str, lambda s: len(s) > 0)}], lambda l: len(l) > 0,
                              error='Invalid value for parameter availablePlatforms'),
}

GAME_UPDATE_SCHEMA = {
    'gameId': And(str, lambda s: len(s) > 0, error='Invalid value for parameter gameId'),
    **GAME_CREATION_SCHEMA
}


class SchemaValidator:
    @staticmethod
    def validate_request(schema: dict, data):
        try:
            Schema(schema).validate(data)
        except SchemaError as ex:
            raise ApiError(error_code=400, error_message=str(ex))


class PlatformSchemaValidator(SchemaValidator):
    def validate_creation_request(self, request):
        self.validate_request(schema=PLATFORM_CREATION_SCHEMA, data=request)

    def validate_update_request(self, request):
        self.validate_request(schema=PLATFORM_UPDATE_SCHEMA, data=request)


class GameSchemaValidator(SchemaValidator):
    def validate_creation_request(self, request):
        self.validate_request(schema=GAME_CREATION_SCHEMA, data=request)

    def validate_update_request(self, request):
        self.validate_request(schema=GAME_UPDATE_SCHEMA, data=request)
