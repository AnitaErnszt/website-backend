from utils import bug_response, reg_response
import json, boto3, os

def lambda_handler(event, context):
    #Set up enviroment variables and boto3
    cognito = boto3.client("cognito-idp")
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(os.environ["DYNAMO_TABLE"])
    userpool_id = os.environ["USERPOOL_ID"]
    client_id = os.environ["CLIENT_ID"]

    #Parse payload
    payload = json.loads(event.get("body"))
    email = payload["email"]
    last_name = payload["last_name"]
    first_name = payload["first_name"]
    password = payload["password"]

    #Call Cognito to add user to the user pool
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

    #Verify email address
    try:
        cognito.admin_update_user_attributes(
            UserPoolId=userpool_id,
            Username=email,
            UserAttributes=[{"Name": "email_verified", "Value": "true"}]
        )
    
    except Exception:
        return bug_response("Confirm.Exception")

    #Confirm the sign up. Cognito can only assign token for confirmed users
    try:
        cognito.admin_confirm_sign_up(
            UserPoolId=userpool_id, Username=cognito_response["UserSub"]
            )

    except Exception:
        return bug_response("Confirm.Exception")
    
    #Add user to the database
    try:
        table.put_item(
            Item={
                "id": id,
                "email": email,
                "first_name": first_name,
                "last_name": last_name
            })
        
    except Exception:
        return bug_response("DynamoDB.Exception")
        
    #Login the user after registering them
    auth_response = cognito.initiate_auth(
            ClientId=client_id,
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={"USERNAME": email, "PASSWORD": password},
        )

    #Return API response
    return reg_response(auth_response, payload)
