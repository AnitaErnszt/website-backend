import json
import boto3
from utils import api_respond, bug_response
import os
import uuid

def lambda_handler(event, context):
    print(event)
    body = json.loads(event["body"])
    user_id = body["user_id"]
    player_name = body["player_name"]
    game_time = body["game_time"]
    game_id = str(uuid.uuid4())
    
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(os.environ["DYNAMO_TABLE"])
    
    if user_id == "":
        user_id = "no user_id"
    
    response = table.put_item(
        Item={
            "id": game_id,
            "player_name": player_name,
            "user_id": user_id,
            "game_time": game_time
            }
        )
    
    return api_respond()

