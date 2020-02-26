from json import JSONDecoder, JSONDecodeError
import re
import os
import psycopg2
from psycopg2 import pool

NOT_WHITESPACE = re.compile(r'[^\s]')

def decode_stacked(document, pos=0, decoder=JSONDecoder()):
    while True:
        match = NOT_WHITESPACE.search(document, pos)
        if not match:
            return
        pos = match.start()

        try:
            obj, pos = decoder.raw_decode(document, pos)
        except JSONDecodeError:
            # do something sensible if there's some error
            raise
        yield obj

def create_pg_pool():
    host = os.environ['PGHOST']
    dbname = os.environ['PGDATABASE']
    username = os.environ['PGUSER']
    password = os.environ['PGPASSWORD']
    port = int(os.environ.get('PGPORT', 5432))

    return psycopg2.pool.SimpleConnectionPool(
        1,
        3,
        dbname=dbname,
        user=username,
        password=password,
        host=host,
        port=port
    )

def pg_in_brackets(arr, cur):
    return cur.mogrify('(' + ','.join(['%s'] * len(arr)) + ')', tuple(arr))

def create_pg_conn():
    host = os.environ['PGHOST']
    dbname = os.environ['PGDATABASE']
    username = os.environ['PGUSER']
    password = os.environ['PGPASSWORD']
    
    return psycopg2.connect(
        dbname=dbname,
        user=username,
        password=password,
        host=host
    )