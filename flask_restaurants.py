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
app.config['SECRET_KEY'] = '12212112'

cache = Cache(app, config={"CACHE_TYPE": "simple", "CACHE_DEFAULT_TIMEOUT": 300})
app.config["PERMANENT_SESSION_LIFETIME"]

engine = create_engine("sqlite:///my_mini_project_3_db.db", echo=True )
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

class Dishes(Base, UserMixin):
    __tablename__ = "dishes"
    id: Mapped[int] = mapped_column(primary_key=True)
    dish_name: Mapped[str] = mapped_column(String(80))
    dish_type: Mapped[str] = mapped_column(String(80))
    cost: Mapped[str] = mapped_column(String(80))
    dish_size: Mapped[str] = mapped_column(String(80))
    calories: Mapped[str] = mapped_column(String(80))
    rests: Mapped[int] = mapped_column(ForeignKey("restaurants.id"))

class Restaurants(Base, UserMixin):
    __tablename__ = "restaurants"
    id: Mapped[int] = mapped_column(primary_key=True)
    rests: Mapped[str] = mapped_column(String(80))

class Basket():
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users2.id"))
    favorite_dishes: Mapped[int] = mapped_column(ForeignKey("dishes.id"))


# base = Base()
# base.create_db()

class Form_pg1(flask_wtf.FlaskForm):
    login_sub = SubmitField(label="Увійти", name='log')
    signup_sub = SubmitField(label='Зареєструватися', name='reg')

# class Form_pg2(flask_wtf.FlaskForm):
#     rest_name = StringField("")

class Form_login(flask_wtf.FlaskForm):
    nickname = StringField('nickname', validators=[InputRequired(),])
    password = PasswordField('password', validators=[InputRequired(),])
    submit = SubmitField('login')

class Form_signUp(flask_wtf.FlaskForm):
    nickname = StringField('nickname', validators=[InputRequired(), ])
    email = StringField('email', validators=[InputRequired(),])
    password = PasswordField('password', validators=[InputRequired(), ])
    submit = SubmitField('sign up')

class Form_restaurants(flask_wtf.FlaskForm):
    menu = SubmitField("Меню")

class InTheBasket(flask_wtf.FlaskForm):
    in_the_basket = SubmitField("Додати до кошику")

class Form_backToRestaurants(flask_wtf.FlaskForm):
    to_restaurants = SubmitField("Повернутися до ресторанів")


with Session() as session1:
    new_rest = Restaurants(rests="Restaurant1")
    session1.add(new_rest)
    session1.commit()


@app.route('/', methods=['POST', "GET"])
def f_1():
    form = Form_pg1()
    form_log = Form_login()
    form_sign = Form_signUp()

    if request.method == 'GET':
        return render_template('restaurants_pg1.html', form=form)
    else:
        if 'log' in request.form:
            return render_template('restaurants_pg2.html', form=form_log)
        else:
            return render_template('restaurants_pg3.html', form=form_sign)

@app.route('/login', methods=["POST", "GET"])
def f_2():
    form = Form_login()
    with Session() as session1:
        user = session1.query(Users).filter_by(nickname=form.nickname.data, password=form.password.data).first()
        if user:
            session["user_id"] = user.id
            return redirect(url_for('f_4'))
        else:
            return 'Логін або пароль невірний'

@app.route('/sign_up', methods=["POST", "GET"])
def f_3():
    form = Form_signUp()
    with Session() as session1:
        new_user = Users(nickname=form.nickname.data, email=form.email.data, password=form.password.data)
        session1.add(new_user)
        session1.commit()
        session["user_id"] = new_user.id
        return redirect(url_for('f_4'))

@app.route("/restaurants", methods=["POST", "GET"])
def f_4():
    form = Form_restaurants()
    if request.method == "GET":
        with Session() as session1:
            rests = session1.query(Restaurants).all()
        return render_template("restaurants_pg4.html", data=rests, form=form)

@app.route("/dishes", methods=["POST", "GET"])
def f_5():
    form = InTheBasket()
    if request.method == "POST":
        user_id = session.get("user_id")
        with Session() as session1:
            new_items = Basket(user_id=user_id, favorite_dishes=request.form["rest_id"])
            session1.add(new_items)
            session1.commit()
    with Session() as session2:
        all_dishes = session2.query(Dishes).filter_by(rest_id=request.form["rest_id"])
    return render_template("restaurants_pg5.html", form=form, data=all_dishes)


@app.route("/basket")
def f_6():
    form = Form_backToRestaurants()
    with Session() as session1:
        user_id = session1.get("user_id")
        data = session1.query(Basket).filter_by(user_id=user_id).all()
    return render_template("restaurants_pg6.html", form=form, data=data)


if __name__ == "__main__":
    app.run(debug=True, port=8000)
