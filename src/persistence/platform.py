import uuid
from datetime import datetime

from boto3.dynamodb.conditions import Attr

from persistence.base_repository import BaseRepository

VALID_CREATE_KEYS = ['name', 'subtype']
VALID_CREATE_TYPES = {'name': str, 'subtype': str}

VALID_UPDATE_KEYS = ['name', 'platformId', 'subtype']
VALID_UPDATE_TYPES = {'name': str, 'platformId': str, 'subtype': str}


class Platform:

    def __init__(self, name: str, subtype: str = None, platform_id: str = None, creation_date: int = None,
                 modification_date: int = None):
        self.name = name
        self.subtype = subtype
        self.platform_id = platform_id
        self.creation_date = creation_date
        self.modification_date = modification_date

    def build_to_create(self):
        now = datetime.utcnow()
        self.platform_id = str(uuid.uuid4())
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


class PlatformRepository(BaseRepository):

    def __init__(self):
        super().__init__(table_name='store-platform')

    @staticmethod
    def _build_platform(item: dict) -> Platform:
        return Platform(name=item.get('name'),
                        subtype=item.get('subtype'),
                        platform_id=item.get('platformId'),
                        creation_date=item.get('creationDate'),
                        modification_date=item.get('modificationDate'))

    def save(self, platform: dict):
        self.table.put_item(Item=platform)

    def get(self, platform_id: str):
        response = self.table.get_item(
            Key={
                'platformId': platform_id
            }
        )
        if response.get('Item'):
            return self._build_platform(item=response.get('Item'))
        else:
            return None

    def delete(self, platform_id: str):
        self.table.delete_item(
            Key={
                'platformId': platform_id
            }
        )

    def search(self, name: str = None, sub_type: str = None) -> list:
        if name and sub_type:
            response = self._search_by_name_and_sub_type(name=name, sub_type=sub_type)
        elif name:
            response = self._search_by_name(name=name)
        elif sub_type:
            response = self._search_by_sub_type(sub_type=sub_type)
        else:
            response = self.table.scan()
        items = []
        for item in response.get('Items'):
            items.append(self._build_platform(item=item))
        return items

    def _search_by_name(self, name: str) -> list:
        return self.table.scan(
            FilterExpression=Attr('name').contains(name)
        )

    def _search_by_sub_type(self, sub_type: str) -> list:
        return self.table.scan(
            FilterExpression=Attr('subtype').contains(sub_type)
        )

    def _search_by_name_and_sub_type(self, name: str, sub_type: str) -> list:
        return self.table.scan(
            FilterExpression=Attr('name').contains(name) & Attr('subtype').contains(sub_type)
        )
