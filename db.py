import json
import psycopg2
import config
from random import choice
from time import time

themes = {}
last_id = {}

def conn():
    return psycopg2.connect(f'dbname={config.db_name}  user={config.db_user} password={config.db_password} host={config.db_ip}')

def exec(ask):
    with conn() as db:
        cur=db.cursor()
        cur.execute(ask)
        return cur

def new_user(tel_id, name):
    exec(f"INSERT INTO users (tel_id, name) VALUES ('{tel_id}','{name}')")

#bot interactions

def new_theme(old_themes):
    #return -1 if no more themes
    themes = exec("SELECT id FROM themes").fetchall()
    for old_theme in old_themes:
        themes.remove((old_theme,))
    if themes:
        return choice(themes[0])
    else:
        return -1

def random_question(theme_id):
    questions=exec(f"SELECT quest, id FROM questions WHERE theme_id='{ theme_id }'").fetchall()
    return choice(questions)

def start_poll(tel_id):
    if tel_id not in last_id:
        themes[tel_id] = [new_theme([])]
        quest, last_id[tel_id]= random_question(themes[tel_id][0])
        return quest
    else:
        return -1 #done poll

def next_question(tel_id, ans):
    if tel_id in last_id:
        if ans.isdigit():
            if int(ans)<=9:
                if int(ans)>0:
                    exec(f"INSERT INTO answers (quest_id, ans, time, user_id) VALUES ({last_id[tel_id]}, {ans}, {time()+86400*1}, '{tel_id}')")
                    theme = new_theme(themes[tel_id])
                    if theme != -1:
                        themes[tel_id].append(theme)
                        quest, last_id[tel_id] = random_question(theme)
                        return quest
                    else:
                        return -1 #done poll
        return exec(f"SELECT quest FROM questions WHERE id= {last_id[tel_id]}").fetchone()[0]
    else:
        return start_poll(tel_id)

def all_themes():
    return exec("SELECT theme, id FROM themes").fetchall()

def all_data(theme_id):
    return exec(f'SELECT answers.ans, answers.time FROM answers INNER JOIN questions ON answers.quest_id=questions.id WHERE questions.theme_id = {theme_id}').fetchall()

def personal_data():
    return 0
