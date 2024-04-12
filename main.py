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

print(1)

app = Flask(__name__)

app.config['SECRET_KEY'] = '12212112'

cache = Cache(app, config={"CACHE_TYPE": "simple", "CACHE_DEFAULT_TIMEOUT": 300})
app.config["PERMANENT_SESSION_LIFETIME"]

engine = create_engine("sqlite:///cookies.db", echo=True)
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

@app.route('/', methods = ['POST', "GET"])
def f_1():
    if "user_id" in session:
        return redirect(url_for("f_4"))
    form = Form_pg1()
    form_log = Form_login()
    form_sign = Form_signUp()
    if request.method == 'GET':
        return render_template('cookies_e1_pg1.html', form=form)
    else:
        if 'log' in request.form:
            return render_template('cookies_e1_pg2.html', form=form_log)
        else:
            return render_template('cookies_e1_pg3.html', form=form_sign)


@app.route('/login', methods=['POST'])
def f_2():
    form = Form_login()
    with Session() as session1:
        user = session1.query(Users).filter_by(nickname=form.nickname.data, password=form.password.data).first()
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
        session["user_id"] = new_user.id
        return redirect(url_for('f_4'))

@app.route("/page4", methods = ['POST', "GET"])
def f_4():
    return render_template("cookies_e1_pg4.html")

if __name__ == "__main__":
    app.run(debug=True, port=8000)
