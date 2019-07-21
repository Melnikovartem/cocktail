import json
import psycopg2
import config

def conn():
    return psycopg2.connect(f'dbname={config.db_name}  user={config.db_user} password={config.db_password} host={config.db_ip}'

def exec(ask):
    with conn() as db:
        cur=db.cursor()
        cur.execute(ask)
        return cur
