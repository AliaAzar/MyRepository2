import flask_wtf
from datetime import datetime
import wtforms
from wtforms import StringField, SubmitField, IntegerField, PasswordField, DateField
from wtforms.validators import InputRequired
from flask_login import LoginManager, login_user, logout_user, current_user, login_required, UserMixin
from flask import request, Flask, render_template, url_for, redirect, session
from sqlalchemy import Column, create_engine, String, ForeignKey, Date
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Mapped, mapped_column
from flask_caching import Cache
from flask_wtf import FlaskForm
from bs4 import BeautifulSoup
import requests

r = requests.get("https://osvita.ua/vnz/guide/")

soup = BeautifulSoup(r.content, 'html.parser')

app = Flask(__name__)
app.config["SECRET_KEY"] = "12212112"

engine = create_engine("sqlite:///my_mini_project_4_db.db", echo=True)
Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    def create_db(self):
        Base.metadata.create_all(engine)

    def drop_db(self):
        Base.metadata.drop_all(engine)

class Users(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80))
    email: Mapped[str] = mapped_column(String(80))
    age: Mapped[int] = mapped_column()
    text: Mapped[str] = mapped_column(String(1470))
    university: Mapped[str] = mapped_column(String(210))

# base = Base()
# base.create_db()

class Form_pg1(flask_wtf.FlaskForm):
    name = wtforms.StringField("Введіть ваше ім'я:", validators=[InputRequired(),])
    email = wtforms.StringField("Введіть вашу електронну пошту:", validators=[InputRequired(),])
    age = wtforms.StringField("Введіть ваш вік:", validators=[InputRequired(),])
    text = wtforms.StringField("Введіть текст:", validators=[InputRequired(),])
    submit = wtforms.SubmitField("Готово!")

class Form_application(flask_wtf.FlaskForm):
    submit = wtforms.SubmitField("Подати заявку")


@app.route("/", methods=["POST", "GET"])
def f_1():
    form = Form_application()
    if request.method == "POST":
        session["univer_name"] = request.form["univer"]
        return redirect(url_for("f_2"))
    elif request.method == "GET":
        data = soup.select("a.link-educational")
        return render_template("universities_pg1.html", form=form, data=data)

@app.route("/pg2", methods=["POST", "GET"])
def f_2():
    form = Form_pg1()
    if request.method == "POST":
        with Session() as session1:
            data = Users(name=form.name.data, email=form.email.data, age=form.age.data, text=form.text.data, university=session["univer_name"])
            session1.add(data)
            session1.commit()
            return redirect(url_for("f_1"))
    elif request.method == "GET":
        return render_template("universities_pg2.html", form=form)



if __name__ == "__main__":
    app.run(debug=True, port=8000)
