import uuid
from datetime import datetime

from boto3.dynamodb.conditions import Attr

from configuration.base_repository import BaseRepository


class Game:

    def __init__(self, account: str, name: str, release_date: str, price: float,
                 available_platforms: list = None, description: str = None, game_id: str = None,
                 creation_date: int = None, modification_date: int = None):
        self.account = account
        self.name = name
        self.release_date = release_date
        self.price = price
        self.available_platforms = available_platforms
        self.description = description
        self.game_id = game_id
        self.creation_date = creation_date
        self.modification_date = modification_date

    def build_to_create(self):
        now = datetime.utcnow()
        self.game_id = str(uuid.uuid4())
        self.modification_date = int(datetime.timestamp(now))
        self.creation_date = int(datetime.timestamp(now))
        return self

    def build_to_update(self):
        now = datetime.utcnow()
        self.modification_date = int(datetime.timestamp(now))
        return self

    @staticmethod
    def _to_camel_case(snake_case: str) -> str:
        words = snake_case.split('_')
        return words[0] + ''.join(word.title() for word in words[1:])

    def to_dict(self) -> dict:
        return {self._to_camel_case(key): value for key, value in self.__dict__.items() if value}


class GameRepository(BaseRepository):

    def __init__(self):
        super().__init__(table_name='store-game')

    @staticmethod
    def __build_game(item: dict) -> Game:
        return Game(account=item.get('account'),
                    name=item.get('name'),
                    release_date=item.get('releaseDate'),
                    price=item.get('price'),
                    available_platforms=item.get('availablePlatforms'),
                    description=item.get('description'),
                    game_id=item.get('gameId'),
                    creation_date=item.get('creationDate'),
                    modification_date=item.get('modificationDate'))

    def save(self, game: dict):
        self.table.put_item(Item=game)

    def get(self, account: str, game_id: str):
        response = self.table.get_item(
            Key={
                'account': account,
                'gameId': game_id
            }
        )
        if response.get('Item'):
            return self.__build_game(item=response.get('Item'))
        else:
            return None

    def delete(self, account: str, game_id: str):
        self.table.delete_item(
            Key={
                'account': account,
                'gameId': game_id
            }
        )

    def search(self, name: str = None, validate: bool = False) -> list:
        if validate and name:
            response = self._validate_name(name=name)
        elif name:
            response = self._search_by_name(name=name)
        else:
            response = self.table.scan()
        items = []
        for item in response.get('Items'):
            items.append(self.__build_game(item=item))
        return items

    def _validate_name(self, name: str) -> list:
        return self.table.scan(
            FilterExpression=Attr('name').eq(name)
        )

    def _search_by_name(self, name: str) -> list:
        return self.table.scan(
            FilterExpression=Attr('name').contains(name)
        )
