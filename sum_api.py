import requests
from flask import request, Flask, render_template, url_for, redirect, session, jsonify

api_key = "dfdc337a7cd778a394f0b074f56b24be"

app = Flask(__name__)
app.config["SECRET_KEY"] = "12212112"


@app.route("/")
def f_1():
    return render_template("sum_api.html")

@app.route("/sum")
def f_2():
    num1 = request.args.get("info1")
    num2 = request.args.get("info2")
    sum = int(num1) + int(num2)
    return jsonify({"suma": sum})



if __name__ == "__main__":
    app.run(debug=True, port=8000)
