import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('users')

def create_table():
    # Create the DynamoDB table
    try:
        response = dynamodb.create_table(
            TableName='users',
            KeySchema=[
                {
                    'AttributeName': 'user_id',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'user_id',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        table.wait_until_exists()

    except dynamodb.meta.client.exceptions.ResourceInUseException:
        print("Table already exists.")
        return
    except Exception as e:
        print(f"Error creating table: {e}")
        return

def create_account(user_id="user_1234", chat_context=[]):
    # Create a new user item in the DynamoDB table
    try:
        # Add More Attributes as needed
        response = table.put_item(
            Item={
                'user_id': user_id,
                'chat_context': chat_context
            }
        )
    except Exception as e:
        print(f"Error creating user: {e}")
    return

def save_session(chat_context, user_id="user_1234", user_email=None):
    try:
        table.update_item(
            Key={
                'user_id': user_id
            },
            UpdateExpression="SET chat_context = :val1",
            ExpressionAttributeValues={
                ':val1': chat_context
            }
        )
    except Exception as e:
        print(f"Error updating item: {e}")
    
    return

def load_session(user_id="user_1234", user_email=None):
    try:
        response = table.get_item(
            Key={
                'user_id': user_id
            }
        )
        
        print(f"Loaded session for user {user_id}: {response}")
        return response['Item']['chat_context']
    except Exception as e:
        raise Exception(f"Error getting item: {e}")