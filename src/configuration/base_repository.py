import boto3

resource = boto3.resource('dynamodb',
                          region_name='us-west-2',
                          endpoint_url="http://localhost:8000",
                          aws_access_key_id='key',
                          aws_secret_access_key='key')


class BaseRepository:

    def __init__(self, table_name: str):
        self.table = resource.Table(table_name)
