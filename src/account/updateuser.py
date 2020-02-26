import json
import os
import boto3
from utils import api_respond, bug_response

def lambda_handler(event, context):
    print(event)
    
    request = event.body

    user_id = event["requestContext"]["authorizer"]["claims"]["sub"]

    dynamodb = boto3.client("dynamodb")
    table = os.environ["DYNAMO_TABLE"]

    try:
        response = dynamodb.update_item(
            TableName=table,
            Key={"id": {"S": user_id}}
            UpdateExpression="SET first_name = :fn, last_name = :ln, email = :e, player_name = :pn",
            },
            ExpressionAttributeValues={
                ":fn": {
                    "S": request.first_name
                },
                ":ln": {
                    "S": request.last_name
                },
                ":e": {
                    "S": request.email
                },
                ":pn": {
                    "S": request.player_name
                }
            }
        )
    except Exception:
        return bug_response("User_data.Exception", 404)

    data = {
        "id": user_id,
        "profile": response,
    }

    return api_respond(data)

