import flask_wtf
import wtforms
from wtforms import StringField, SubmitField, IntegerField, PasswordField, DateField
from wtforms.validators import InputRequired
from flask import request, Flask, render_template, url_for, redirect, session
import requests

api_key = "dfdc337a7cd778a394f0b074f56b24be"

app = Flask(__name__)
app.config["SECRET_KEY"] = "12212112"

class Form_city(flask_wtf.FlaskForm):
    city = wtforms.StringField("Введіть місто:", validators=[wtforms.validators.InputRequired(),])
    submit = wtforms.SubmitField("Дізнатися погоду")

class Form_seeHistory(flask_wtf.FlaskForm):
    toHistory = SubmitField("Перейти до вашої історії", validators=[wtforms.validators.InputRequired(),])

@app.route("/", methods=["POST", "GET"])
def f_1():
    form = Form_city()
    if request.method == "GET":
        return render_template("weather_pg1.html", form=form)
    else:
        city = request.form["city"]
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        responce = requests.get(url)
        if responce.ok:
            data = responce.json()
            session1 = session.get("list", [])
            if city not in session1:
                session1.append(city)
                session["list"] = session1
            return render_template("weather_pg2.html", data=data)
        else:
            return "Щось пішло не так..."

@app.route("/history", methods=["POST", "GET"])
def f_2():
    session2 = session.get("list", [])
    if session2:
        return f"Усі міста, у яких ви дізнавалися погоду: {session2}"
    else:
        return "Ви ще не дізнавалися міста"

if __name__ == "__main__":
    app.run(debug=True, port=8000)
