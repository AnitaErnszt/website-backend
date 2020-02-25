import json, boto3
from utils import api_respond

def lambda_handler(event, context):
    email = json.loads(event["body"])
    print(email)
    ses = boto3.client("ses")
    
    email_to_me = '''<p>You have received the following email on your website:</p>
    <br>
    <p>Sender: ''' + email["sender"] + ''',</p>
    <p>Subject: ''' + email["subject"] + ''',</p>
    <p>Message: ''' + email["message"] + '''</p>'''
    
    response = ses.send_email(
        Source="mosolyognijo@gmail.com",
        Destination={
            "ToAddresses": [
                "anita.ernszt@gmail.com",
            ]
        },
        Message={
            "Subject": {
                "Data": email["subject"]
            },
            "Body": {
                "Html": {
                    "Data": email_to_me
                }
            }
        },
        SourceArn="arn:aws:ses:eu-west-1:009648319683:identity/mosolyognijo@gmail.com"
    )

    return api_respond()

