import flask_wtf
from datetime import datetime
from wtforms import StringField, SubmitField, IntegerField, PasswordField, DateField
from wtforms.validators import InputRequired
from flask_login import LoginManager, login_user, logout_user, current_user, login_required, UserMixin
from flask import request, Flask, render_template, url_for, redirect, session
from sqlalchemy import Column, create_engine, String, ForeignKey, Date
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Mapped, mapped_column
from flask_caching import Cache
from flask_wtf import FlaskForm

app = Flask(__name__)

cache = Cache(app, config={"CACHE_TYPE": "simple", "CACHE_DEFAULT_TIMEOUT": 300})
app.config["PERMANENT_SESSION_LIFETIME"]

engine = create_engine("sqlite:///cookies.db", echo=True )
Session = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    def create_db(self):
        Base.metadata.create_all(engine)

    def drop_db(self):
        Base.metadata.drop_all(engine)

class Users(Base, UserMixin):
    __tablename__ = "users2"
    id: Mapped[int] = mapped_column(primary_key=True)
    nickname: Mapped[str] = mapped_column(String(80))
    email: Mapped[str] = mapped_column(String(80))
    password: Mapped[str] = mapped_column(String(80))

class Costs(Base, UserMixin):
    __tablename__ = "users3"
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(80))
    sum: Mapped[str] = mapped_column(String(80))
    date = Column("date", Date)
    user_id: Mapped[str] = mapped_column(String(80))

class Form_Costs(flask_wtf, FlaskForm):
    text = StringField(name="text")
    sum = StringField(name="sum")
    date = DateField


class Events(Base):
    __tablename__ = "events"
    id: Mapped[int] = mapped_column(primary_key=True)
    header: Mapped[str] = mapped_column(String(80))
    date = Column("date", Date)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

# base = Base()
# base.create_db()

class Form_pg1(flask_wtf.FlaskForm):
    login_sub = SubmitField(label="Увійти", name='log')
    signup_sub = SubmitField(label='Зареєструватися', name='reg')

class Form_login(flask_wtf.FlaskForm):
    nickname = StringField('nickname', validators=[InputRequired(),])
    password = PasswordField('password', validators=[InputRequired(),])
    submit = SubmitField('login')

class Form_signUp(flask_wtf.FlaskForm):
    nickname = StringField('nickname', validators=[InputRequired(), ])
    email = StringField('email', validators=[InputRequired(),])
    password = PasswordField('password', validators=[InputRequired(), ])
    submit = SubmitField('sign up')

class Form_sum(flask_wtf.FlaskForm):
    submit = SubmitField("Сума витрат")


@app.route('/', methods = ['POST', "GET"])
def f_1():
    form = Form_pg1()
    form_log = Form_login()
    form_sign = Form_signUp()
    if request.method == 'GET':
        return render_template('calendar_pg1.html', form = form)
    else:
        if 'log' in request.form:
            return render_template('calendar_pg2.html',form = form_log)
        else:
            return render_template('calendar_pg3.html', form = form_sign)

@app.route('/login', methods = ['POST'])
def f_2():
    form = Form_login()
    with Session() as session1:
        user = session1.query(Users).filter_by(nickname = form.nickname.data, password = form.password.data).first()
        if user:
            session1["user_id"] = user.id
            return redirect(url_for('f_4'))
        else:
            return 'Логін або пароль невірний'

@app.route('/sign_up', methods = ['POST'])
def f_3():
    form = Form_signUp()
    with Session() as session1:
        new_user = Users(nickname=form.nickname.data, email=form.email.data, password=form.password.data)
        session1.add(new_user)
        session1.commit()
        session1["user_id"] = new_user.id
        return redirect(url_for('f_4'))

@app.route("/costs", methods=["POST", "GET"])
def f_4():
    user_id = session.get("user_id")
    current_data = datetime.now().date()
    form = Form_sum
    with Session() as session1:
        us_events = session1.query(Costs).filter_by(user_id=user_id).all()
    return render_template('calendar_pg4.html', costs=us_events, form=form)

@app.route("/sum_costs")
def f_5():
    user_id = session.get("user_id")
    sum = cache.get(f"all_sum{user_id}")
    if not sum:
        with Session() as session1:
            user_id = session1.get("user_id")
            costs = session1.query(Costs).filter_by(user_id=user_id).all()
            sum = 0
            for i in costs:
                sum += int(i.sum)
            cache.set(f"all_sum{user_id}", sum)
    return sum

@app.route('/add_event', methods = ['POST','GET'])
def f_5():
    user_id = current_user.get_id()
    form = Form_add_event()
    if request.method == 'GET':
        return render_template('calendar_pg5.html', form=form)
    else:
        with Session() as session1:
            new_event = Events(header=form.header.data, date=form.date.data, user_id=user_id)
            session1.add(new_event)
            session1.commit()
        return redirect(url_for('f_4'))


if __name__ == '__main__':
    app.run(debug=True, port=8000)
