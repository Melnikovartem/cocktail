from flask import Flask, render_template
from db import all_themes, all_data

from datetime import datetime

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


if __name__ == "__main__":
    app.run()
