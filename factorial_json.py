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

class Factorial(Base):
    __tablename__ = "factorial"
    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[int] = mapped_column()
    factorial: Mapped[int] = mapped_column()

@app.route("/", methods=["POST", "GET"])
def f_1():
    return render_template("factorial_json_pg1.html")

@app.route("/pg2")
def f_2():
    print(2111112113121123213231231231231231231231232132132131231232132)
    number = request.args.get("num")
    factorial = request.args.get("factorial")
    factorial1 = 1
    print(factorial)
    for i in range(1, int(number) + 1):
        factorial1 = factorial1 * i
        print(i)
        print(factorial1)
    if int(factorial1) == int(factorial):
        with Session() as session1:
            number = session1.query(Factorial).filter_by(number=number)
            if number:
                return jsonify({"answer": "Факторіал цього числа вже записан"})
            else:
                new_factorial = Factorial(number=number, factorial=factorial)
                session1.add(new_factorial)
                session1.commit()
                return jsonify({"answer": "Факторіал числа був успішно записан"})
    else:
        return jsonify({"answer": "Ви написали неправильний факторіал"})


if __name__ == "__main__":
    app.run(debug=True, port=8000)
