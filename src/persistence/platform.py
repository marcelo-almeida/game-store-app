import uuid
from datetime import datetime

from boto3.dynamodb.conditions import Attr

from persistence.base_repository import BaseRepository

VALID_CREATE_KEYS = ['name', 'subtype']
VALID_CREATE_TYPES = {'name': str, 'subtype': str}

VALID_UPDATE_KEYS = ['name', 'platformId', 'subtype']
VALID_UPDATE_TYPES = {'name': str, 'platformId': str, 'subtype': str}


class Platform:

    def __init__(self, request: dict):
        now = datetime.utcnow()
        self.platform_id = request['platformId'] \
            if 'platformId' in request else str(uuid.uuid4())
        self.name = request['name']
        self.subtype = request['subtype'] if 'subtype' in request else None
        self.modification_date = request['modificationDate'] \
            if 'modificationDate' in request else int(datetime.timestamp(now))
        self.creation_date = request['creationDate'] \
            if 'creationDate' in request else int(datetime.timestamp(now))

    @staticmethod
    def _to_camel_case(snake_case: str) -> str:
        words = snake_case.split('_')
        return words[0] + ''.join(word.title() for word in words[1:])

    def to_dict(self) -> dict:
        return {self._to_camel_case(key): value for key, value in self.__dict__.items() if value}


class PlatformRepository(BaseRepository):

    def __init__(self):
        super().__init__(table_name='store-platform')

    def save(self, platform: dict):
        self.table.put_item(Item=platform)

    def get(self, platform_id: str) -> dict:
        response = self.table.get_item(
            Key={
                'platformId': platform_id
            }
        )
        return response.get('Item')

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
        return response.get('Items')

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
