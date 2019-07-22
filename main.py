from flask import Flask, render_template
from db import all_themes, all_data, all_data_period, get_user, personal_data_period, get_theme, all_data_user, all_users

from datetime import datetime

from re import match

import config

from time import mktime

app = Flask(__name__)

@app.route("/")
def index():
    data = []
    themes, themes_id = zip(*all_themes())
    users = all_users()
    for user in users:
        ans = []
        time = []
        for theme in themes_id:
            ans1, _ = zip(*all_data_user(theme, user))
            ans.append(ans1[0])
        data.append([get_user(user), ans ,themes])
    return render_template("index.html", data=data)

@app.route("/<user>")
def user_scatter(user):
    data = []
    themes, themes_id = zip(*all_themes())
    ans =[]
    for theme in themes_id:
        ans1, _ = zip(*all_data_user(theme, user))
        ans.append(ans1[0])
    data.append([get_user(user), ans ,themes])
    return render_template("user.html", data=data)

if __name__ == "__main__":
    app.run(threaded=True, host=config.web_ip, port=config.port)
