from utils import bug_response, response_data
import json, boto3, os

def lambda_handler(event, context):
    #Set up enviroment variables and boto3
    cognito = boto3.client("cognito-idp")
    client_id = os.environ["CLIENT_ID"]
    table = os.environ["DYNAMO_TABLE"]

    #Parse payload
    payload = json.loads(event.get("body"))
    email = payload.get("email")
    password = payload.get("password")

    #Authenticate the user
    try:
        auth_response = cognito.initiate_auth(
            ClientId=client_id,
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={"USERNAME": email, "PASSWORD": password},
        )

    except cognito.exceptions.InvalidParameterException:
        return bug_response("InvalidParameterException")

    except cognito.exceptions.NotAuthorizedException:
        return bug_response("NotAuthorizedException", 401)

    except cognito.exceptions.PasswordResetRequiredException:
        return bug_response("PasswordResetRequiredException")

    except cognito.exceptions.UserNotConfirmedException:
        return bug_response("UserNotConfirmedException")

    except cognito.exceptions.UserNotFoundException:
        return bug_response("UserNotFoundException")

    except Exception:
        return bug_response("Token.Exception")

    #Return API response
    return response_data(auth_response, table)
