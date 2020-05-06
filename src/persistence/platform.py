from boto3.dynamodb.conditions import Attr

from persistence.base_repository import BaseRepository


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
