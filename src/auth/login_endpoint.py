from utils import api_respond, bug_response, auth_response
import json
import boto3
import os
from jose import jwt

def lambda_handler(event, context):
    cognito = boto3.client("cognito-idp")
    client_id = os.environ["CLIENT_ID"]
    table = os.environ["DYNAMO_TABLE"]

    request_body = json.loads(event.get("body"))

    email = request_body.get("email")
    password = request_body.get("password")

    try:
        session_response = cognito.initiate_auth(
            ClientId=client_id,
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={"USERNAME": email, "PASSWORD": password},
        )

        id_token = session_response["AuthenticationResult"]["IdToken"]
        refresh_token = session_response["AuthenticationResult"]["RefreshToken"]

        session = {"id_token": id_token, "refresh_token": refresh_token}
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

    claims = jwt.get_unverified_claims(id_token)
    id = claims.get("sub")
    
    data = auth_response(id, session, table=table)

    return api_respond(data)

