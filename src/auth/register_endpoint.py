from utils import api_respond, bug_response, auth_response
import os
import json
import boto3
from datetime import date

def lambda_handler(event, context):
    print(event)
    cognito = boto3.client("cognito-idp")
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(os.environ["DYNAMO_TABLE"])
    userpool_id = os.environ["USERPOOL_ID"]
    client_id = os.environ["CLIENT_ID"]

    body = json.loads(event.get("body"))

    email = body["email"]
    last_name = body["last_name"]
    first_name = body["first_name"]
    password = body["password"]

    # Calls Cognito to add user to the user pool

    try:
        cognito_response = cognito.sign_up(
            ClientId=client_id,
            Username=email,
            Password=password,
            UserAttributes=[
                {"Name": "email", "Value": email},
                {"Name": "family_name", "Value": last_name},
                {"Name": "given_name", "Value": first_name},
            ],
        )

        id = cognito_response["UserSub"]

    except cognito.exceptions.UsernameExistsException:
        return bug_response("UsernameExistsException")

    except cognito.exceptions.InvalidPasswordException:
        return bug_response("InvalidPasswordException")

    except cognito.exceptions.InvalidParameterException:
        return bug_response("InvalidParameterException")

    except KeyError:
        return bug_response("KeyError")

    except Exception:
        return bug_response("Signup.Exception")

    verify_email_response = cognito.admin_update_user_attributes(
        UserPoolId=userpool_id,
        Username=email,
        UserAttributes=[{"Name": "email_verified", "Value": "true"},],
    )

    # Confirms the sign up. Cognito can only assign token for confirmed users

    try:
        confirm_signup = cognito.admin_confirm_sign_up(
            UserPoolId=userpool_id, Username=cognito_response["UserSub"]
        )

    except cognito.exceptions.InvalidParameterException:
        return bug_response("InvalidParameterException", email)

    except cognito.exceptions.NotAuthorizedException:
        return bug_response("NotAuthorizedException")

    except cognito.exceptions.UserNotFoundException:
        return bug_response("UserNotFoundException")

    except Exception:
        return bug_response("Confirm.Exception")

    # Provide session tokens for users
    try:
        session_response = cognito.admin_initiate_auth(
            UserPoolId=userpool_id,
            ClientId=client_id,
            AuthFlow="ADMIN_USER_PASSWORD_AUTH",
            AuthParameters={"USERNAME": email, "PASSWORD": password},
        )
        session = {
            "id_token": session_response["AuthenticationResult"]["IdToken"],
            "refresh_token": session_response["AuthenticationResult"]["RefreshToken"],
        }

    except cognito.exceptions.InvalidParameterException:
        return bug_response("InvalidParameterException")

    except cognito.exceptions.NotAuthorizedException:
        return bug_response("NotAuthorizedException")

    except cognito.exceptions.PasswordResetRequiredException:
        return bug_response("PasswordResetRequiredException")

    except cognito.exceptions.UserNotConfirmedException:
        return bug_response("UserNotConfirmedException")
        
    except cognito.exceptions.UserNotFoundException:
        return bug_response("UserNotFoundException")

    except Exception:
        return bug_response("Token.Exception")

    # Add user to the database
    try:
        dynamo_response = table.put_item(
            Item={
                "id": id,
                "email": email,
                "first_name": first_name,
                "last_name": last_name
            }
        )
    except Exception:
        return bug_response("DynamoDB.Exception")

    verify_email_response = cognito.admin_update_user_attributes(
        UserPoolId=userpool_id,
        Username=email,
        UserAttributes=[{"Name": "email_verified", "Value": "true"},],
    )

    user = {"first_name": first_name, "last_name": last_name, "email": email}
    data = auth_response(id, session, user=user)

    return api_respond(data)

