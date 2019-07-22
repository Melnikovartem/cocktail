from flask import Flask, render_template
from db import all_themes, all_data, all_data_period, get_user, personal_data_period, get_theme, all_data_user

from datetime import datetime

from re import match

import config

from time import mktime

app = Flask(__name__)


@app.route("/")
def index():
    data = []
    themes = all_themes()
    for theme in themes:
        all = all_data(theme[1])
        time = []
        time_count = {}
        ans =[]
        for one in all:
            format_time = datetime.fromtimestamp(one[1]).strftime("%m-%d")
            if format_time not in time:
                time.append(format_time)
                time_count[format_time]=[]
            time_count[format_time].append(one[0])
        for time_val in time_count:
            ans.append(sum(time_count[time_val])/len(time_count[time_val]))
        data.append([theme[0], ans, time])
    return render_template("index.html", data=data)

@app.route("/<tel_id>")
def user_scatter(tel_id):
    data = []
    themes = all_themes()
    for theme in themes:
        ans, time = zip(*all_data_user(theme[1], tel_id))
        time = list(map(lambda x:datetime.fromtimestamp(x).strftime("%m-%d"), time))
        data.append([theme[0], list(ans), time])
    return render_template("user.html", data=data)

@app.route("/pie/all_users/<date>")
def all_users_pie(date):
    if not(len(date)==10 and match("\d\d\d\d.\d\d.\d\d",date)):
        return "BAD data try 2019.01.01"
    else:
        date=datetime.strptime(date,'%Y.%m.%d').timestamp()
        all = all_data_period(date)
        data = {}
        themes,_ =zip(*all_themes())
        i=0
        for one in all:
            user=get_user(one[1])
            if user in data:
                data[user][get_theme(one[2])]=one[0]
            else:
                data[user]={get_theme(one[2]):one[0]}
                i+=1
            data[user]["row"] = i//config.cols
            data[user]["col"] = i%config.cols
        dates=[datetime.fromtimestamp(date-86400).strftime('%Y.%m.%d'),datetime.fromtimestamp(date).strftime('%Y.%m.%d'),datetime.fromtimestamp(date+86400).strftime('%Y.%m.%d')]
        return render_template("pie.all_users.html", data=data, themes=themes, rows=len(data.keys())//config.cols+(1 if len(data.keys())%config.cols else 0), cols=config.cols , dates=dates)

@app.route("/pie/<tel_id>/<date>")
def user_pie(tel_id, date):
    if not(len(date)==10 and match("\d\d\d\d.\d\d.\d\d",date)):
        return "BAD data try 2019.01.01"
    else:
        data = {}
        date=datetime.strptime(date,'%Y.%m.%d').timestamp()
        all = personal_data_period(date, tel_id)
        themes,_ =zip(*all_themes())
        for one in all:
            data[get_theme(one[1])]=one[0]
        dates=[datetime.fromtimestamp(date-86400).strftime('%Y.%m.%d'),datetime.fromtimestamp(date).strftime('%Y.%m.%d'),datetime.fromtimestamp(date+86400).strftime('%Y.%m.%d')]
        print(tel_id)
        return render_template("pie.user.html", data=data, themes=themes, user=get_user(tel_id), dates=dates, tel_id=tel_id)


if __name__ == "__main__":
    app.run(threaded=True, host=config.web_ip, port=config.port)
