import json, os, psycopg2

def lambda_handler(event, context):
    rds_address = os.environ["HOST"]
    username = os.environ["DBUSERNAME"]
    password = os.environ["DBPASSWORD"]
    db_name = os.environ["DBNAME"]

    conn = psycopg2.connect(host=rds_address, dbname=db_name, user=username, password=password)
    
    command = (
        """
        CREATE TABLE jsgame_results (
        game_id VARCHAR(256) PRIMARY KEY ,
        player_name VARCHAR(256),
        player_id VARCHAR(30),
        timestamp TIMESTAMP,
        game_time NUMERIC
        """)

    cur = conn.cursor()
    cur.execute(command)
    cur.close()
    conn.commit()
    conn.close()
    
    return "OK"
