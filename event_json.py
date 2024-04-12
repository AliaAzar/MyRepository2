from datetime import datetime
from flask import request, Flask, render_template, url_for, redirect, session
from sqlalchemy import Column, create_engine, String, ForeignKey, Date
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Mapped, mapped_column
from flask import request, Flask, render_template, url_for, redirect, session, jsonify

app = Flask(__name__)

app.config['SECRET_KEY'] = '12212112'

app.config["PERMANENT_SESSION_LIFETIME"]

engine = create_engine("sqlite:///cookies.db", echo=True)
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
    password: Mapped[str] = mapped_column(String(80))

class Events(Base):
    __tablename__ = "events"
    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[str] = mapped_column(String(80))
    text: Mapped[str] = mapped_column(String(80))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))


@app.route("/", methods=["POST", "GET"])
def f_1():
    return render_template("events_json_pg1.html")

@app.route("/login", methods=["POST", "GET"])
def f_2():
    name = request.args.get("name")
    email = request.args.get("email")
    password = request.args.get("password")
    with Session() as session1:
        user = session1.query(Users).filter_by(name=name, email=email, password=password).first()
    if user:
        return jsonify({"login": "Ви успішно війшли в аккаунт"})
    else:
        return "Ви ще не зареестровані"

@app.route("/sign_up", methods=["POST", "GET"])
def f_3():
    name = request.args.get("name")
    email = request.args.get("email")
    password = request.args.get("password")
    with Session() as session1:
        new_user = Users(name=name, email=email, password=password)
        session1.add(new_user)
        session1.commit()
        session["user_id"] = new_user.id
    return jsonify({"signUp": "Ви успішно зареєстровані"})

@app.route("/events", methods=["POST", "GET"])
def f_4():
    with Session() as session1:
        session1.query()
    return render_template("user_events.html")

@app.route("/user_events", methods=["POST", "GET"])
def f_5():
    date = request.args.get("date")
    text = request.args.get("text")
    user_id = session.get("user_id")
    with Session() as session1:
        new_event = Events(date=date, text=text, user_id=user_id)
        session1.add(new_event)
        session1.commit()


if __name__ == "__main__":
    app.run(debug=True, port=8000)

