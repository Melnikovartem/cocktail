from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", x_data=[1,2,3], y_data=[2,4,6])


if __name__ == "__main__":
    app.run()
