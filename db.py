import json
import psycopg2
import config
from time import time, ctime

polls = {}

def conn():
    return psycopg2.connect(f'dbname={config.db_name}  user={config.db_user} password={config.db_password} host={config.db_ip}')

def exec(ask):
    with conn() as db:
        cur=db.cursor()
        cur.execute(ask)
        return cur

def new_user(tel_id, name):
    exec(f"INSERT INTO users (tel_id, name) VALUES ('{tel_id}','{name}'")

def set_admin(tel_id, secret_key):
    if secret_key == config.secret_key:
        exec(f"UPDATE users SET admin=1 WHERE tel_id='{tel_id}'")

def gen_poll(question_id):
    return [exec(f'SELECT quest FROM question WHERE id = {question_id}').fetchone()[0]] + exec(f'SELECT ans FROM answer WHERE quest_id = {question_id}')

def list_polls():
    #make new list of questions by gen_poll
    return [1, [], [], []]

def cur_quest(tel_id):
    return polls[tel_id][polls[tel_id][0]]

def start_poll(tel_id):
    if exec(f"SELECT * FROM users WHERE tel_id='{tel_id}'").fetchone():
        if tel_id not in polls:
            if len(polls[tel_id])>=polls[tel_id][0]+1:
                polls[tel_id] = list_polls()
                return gen_poll(cur_quest(tel_id))
            return "-1" #end of poll
        return "-3" #didnt start poll
    return "-2" # no such user

def new_question(tel_id, text):
    if tel_id not in polls:
        return start_poll(tel_id)
    else:
        if text in polls[tel_id]:
            quest_id = exec(f"SELECT id FROM question WHERE quest = '{cur_quest(tel_id)}'").fecthone()[0]
            ans_id = exec(f"SELECT id FROM answer WHERE ans = '{text}'").fecthone()[0]
            exec(f'INSERT INTO user_answer (quest_id, ans_id, time) VALUES ({quest_id}, {ans_id}, {ctime(time())})')
            polls[tel_id][0] += 1
            if len(polls[tel_id])>=polls[tel_id][0]+1:
                return cur_quest(tel_id)
            else:
                return "-1"
