import json
import boto3

error = {
    "Too_young": "Have to be 18 too register.",
    "UsernameExistsException": "This email is already registered.",
    "InvalidPasswordException": "Password has to be min 8 character log, and must contain upper and lowecase letters and numbers.",
    "Request_criteria": "At least one of the following criteria is required: first_name, last_name, marketing",
    "KeyError": "Mandatory parameter is missing for user registration.",
    "Signup.Exception": "There was an issue creating the user.",
    "DynamoDB.Exception": "There was an issue with adding user to database.",
    "Confirm.Exception": "There was an issue with confirming the user.",
    "InvalidParameterException": "One or more parameter is invalid",
    "NotAuthorizedException": "Invalid email and password combination",
    "UserNotFoundException": "This user is not registered",
    "UserNotConfirmedException": "User is not confirmed",
    "ExpiredCodeException": "The provided verification code is invalid.",
    "PasswordResetRequiredException": "Password reset is required",
    "Token.Exception": "Token request has failed",
    "User_data.Exception": "There was an issue retrieving the user data",
    "LimitExceededException": "You have exceeded the password reset limit. Please wait 24 hrs before you can try again.",
    "Savings.Goal": "Saving goal required",
    "Savings.Months": "Please input how many months you'd like to save",
    "Savings.Start_date": "The earliest you can start your saving plan is today",
    "Other": "Other, not classified error",
}


def api_respond(response=None, status_code=200):
    status = "success" if (status_code >= 200 and status_code < 300) else "failure"
    body = {"status": status}
    if status == "failure":
        body["error"] = response
    elif response is not None:
        body["data"] = response
    return {
        "statusCode": status_code,
        "headers": cors_headers(),
        "body": json.dumps(body),
    }


def bug_response(bug, status_code=400):
    error_response = error.get(bug)
    if error_response is None:
        error_response = error["Other"]
    print("StatusCode:", status_code)
    print("Error message:", error_response)
    return api_respond(error_response, status_code)


def cors_headers():
    return {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "OPTIONS,GET,POST",
        "Access-Control-Allow-Headers": "Authorization,Content-Type,Origin",
    }

def parse_dynamo_type(val_obj):
    for val_type, val in val_obj.items():
        if val_type == "S":
            return val
        elif val_type == "N":
            return int(val)
        elif val_type == "BOOL":
            return bool(val)
        elif val_type == "L":
            return map(parse_dynamo_type, val)
        elif val_type == "M":
            return {
                map_key: parse_dynamo_type(map_val) for map_key, map_val in val.items()
            }
        return None


def parse_dynamo_response(response):
    res_dict = {}
    if not response.get("Item"):
        return None

    item = response["Item"]

    for key, val_obj in item.items():
        res_dict[key] = parse_dynamo_type(val_obj)

    return res_dict
    
    
def reg_response(auth_response, payload):
    authentication = auth_response["AuthenticationResult"]
    data = {"session": return_tokens(authentication),
            "user": payload
    }
    return api_respond(data)


def response_data(auth_response, table):
    authentication = auth_response["AuthenticationResult"]
    data = {"session": return_tokens(authentication),
            "user": return_user(authentication, table)
    }
    return api_respond(data)
    

def return_tokens(authentication):
    tokens = {"refresh_token": authentication.get("RefreshToken"),
            "id_token": authentication["IdToken"]}
    return tokens
    
    
def return_user(authentication, table):
    user_id = get_user_id(authentication["AccessToken"])
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table)
    
    response = table.get_item(
        Key={
            "id": user_id
        })
    return response["Item"]
    
    
def get_user_id(acces_token):
    cognito = boto3.client("cognito-idp")
    response = cognito.get_user(
        AccessToken=acces_token
        )
    user_id = response["Username"]
    return user_id
