from utils import api_respond, bug_response
import json
import psycopg2
import os

def lambda_handler(event, context):
    rds_database = os.environ["PGHOST"]
    username = os.environ["PGUSER"]
    password = os.environ["PGPASSWORD"]
    db_name = os.environ["PGDATABASE"]
    

    return api_respond(data)

