import boto3
from botocore.errorfactory import ClientError

client = boto3.client('dynamodb',
                      region_name='us-west-2',
                      endpoint_url="http://localhost:8000",
                      aws_access_key_id='key',
                      aws_secret_access_key='key')


def _create_game_table():
    client.create_table(
        TableName='store-game',
        AttributeDefinitions=[
            {
                'AttributeName': 'account',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'gameId',
                'AttributeType': 'S'
            }
        ],
        KeySchema=[
            {
                'AttributeName': 'account',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'gameId',
                'KeyType': 'RANGE'
            }
        ],
        BillingMode='PROVISIONED',
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )


def _create_platform_table():
    client.create_table(
        TableName='store-platform',
        AttributeDefinitions=[
            {
                'AttributeName': 'platformId',
                'AttributeType': 'S'
            }
        ],
        KeySchema=[
            {
                'AttributeName': 'platformId',
                'KeyType': 'HASH'
            }
        ],
        BillingMode='PROVISIONED',
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )


def _check_if_exists(table_name: str) -> bool:
    try:
        client.describe_table(
            TableName=table_name
        )
        return True
    except ClientError:
        return False


def create_tables():
    if not _check_if_exists(table_name='store-game'):
        _create_game_table()

    if not _check_if_exists(table_name='store-platform'):
        _create_platform_table()


if __name__ == '__main__':
    create_tables()
