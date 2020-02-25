import json
from utils import api_respond, bug_response
import os
import psycopg2
import datetime
import uuid

def lambda_handler(event, context):
    print(event["body"])
    rds_database = os.environ["PGHOST"]
    username = os.environ["PGUSER"]
    password = os.environ["PGPASSWORD"]
    db_name = os.environ["PGDATABASE"]
    
    body = json.loads(event["body"])
    game_data_list = []
        
    game_data = {
        "game_id": str(uuid.uuid4()),
        "player_name": body.get("player_name"),
        "timestamp": datetime.datetime.now(),
        "game_level": body.get("game_level")}
        
    for key in game_data:
        game_data_list.append(game_data[key])
          
    conn = psycopg2.connect(host=rds_database, dbname=db_name, user=username, password=password)
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO jsgame_results (game_id, player_name, timestamp, game_level)
        VALUES (%s, %s, %s, %s)""", game_data_list)
    cur.close()
    conn.commit()
    
    return api_respond()
