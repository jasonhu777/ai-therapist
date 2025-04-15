import boto3

dynamodb = boto3.resource('dynamodb')

def create_account(data):
    return