import json
import os
import boto3
from utils import api_respond, bug_response

def lambda_handler(event, context):
    profile = {}
    user_id =  event["requestContext"]["authorizer"]["claims"]["sub"]

    dynamodb = boto3.client("dynamodb")
    table = os.environ["DYNAMO_TABLE"]

    try:
        response = dynamodb.get_item(
            TableName=table, Key={"id": {"S": user_id}}
        )
    except Exception:
        return bug_response("User_data.Exception", 404)
        
    for item in response["Item"]:
        profile[item] = response["Item"][item]["S"]

    data = {
        "id": user_id,
        "profile": profile,
    }

    return api_respond(data)

