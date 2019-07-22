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
        ans = []
        for one in all:
            time.append(datetime.fromtimestamp(one[1]).strftime("%m-%d"))
            ans.append(one[0])
        data.append([theme[0], ans, time])

    return render_template("index.html", data=data)


if __name__ == "__main__":
    app.run()
