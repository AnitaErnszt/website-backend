from utils import api_respond, bug_response
import json, psycopg2, os

def lambda_handler(event, context):
    rds_address = os.environ["HOST"]
    username = os.environ["DBUSERNAME"]
    password = os.environ["DBPASSWORD"]
    db_name = os.environ["DBNAME"]

    conn = psycopg2.connect(host=rds_address, dbname=db_name, user=username, password=password)
    

    return api_respond(data)

