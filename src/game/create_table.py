import json
import os
import psycopg2

def lambda_handler(event, context):
    rds_database = os.environ["PGHOST"]
    username = os.environ["PGUSER"]
    password = os.environ["PGPASSWORD"]
    db_name = os.environ["PGDATABASE"]

    conn = psycopg2.connect(host=rds_database, dbname=db_name, user=username, password=password)
    
    command = (
        """
        CREATE TABLE jsgame_results (
        game_id VARCHAR(256) PRIMARY KEY ,
        player_name VARCHAR(256),
        timestamp TIMESTAMP,
        game_level NUMERIC(3,0))
        """)

    cur = conn.cursor()
    cur.execute(command)
    cur.close()
    conn.commit()
    conn.close()
    
    return "OK"
