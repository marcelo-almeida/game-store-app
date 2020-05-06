from persistence.base_repository import BaseRepository


class PlatformRepository(BaseRepository):

    def __init__(self):
        super().__init__(table_name='store-game')

    def save(self, game: dict):
        self.table.put_item(Item=game)

    def get(self, account: str, game_id: str) -> dict:
        response = self.table.get_item(
            Key={
                'account': account,
                'gameId': game_id
            }
        )
        return response.get('Item')

    def delete(self, account: str, game_id: str):
        self.table.delete_item(
            Key={
                'account': account,
                'gameId': game_id
            }
        )

    def search(self) -> list:
        # TODO: define filters for search
        response = self.table.scan()
        return response.get('Items')
