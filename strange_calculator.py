import flask_wtf
import wtforms
from flask import Flask, render_template, request
from flask_caching import Cache

# app = Flask(__name__)
#
# cache = Cache(app, config={"CACHE_TYPE": "simple", "CACHE_DEFAULT_TIMEOUT": 300})
#
# class Nums(flask_wtf.FlaskForm):
#     num = wtforms.IntegerField("Введіть число, пари множників якого ви хочете дізнатися",
#                                validators=[wtforms.validators.InputRequired()])
#     submit = wtforms.SubmitField("Готово!")
#
#
#
# if __name__ == '__main__':
#     app.run(port=8000) # , debug=True

# cache = Cache(app, config={"CACHE_TYPE": "simple", "CACHE_DEFAULT_TIMEOUT": 300})
#
# class Nums(flask_wtf.FlaskForm):
#     first_num = wtforms.IntegerField("Введіть перше число", validators=[wtforms.validators.InputRequired()])
#     second_num = wtforms.IntegerField("Введіть друге число", validators=[wtforms.validators.InputRequired()])
#     submit = wtforms.SubmitField("Готово!")
#
# @app.route("/", methods=["POST", "GET"])
# def f1():
#     form = Nums()
#     return render_template("my_file_1.html", form=form)
#
# @app.route("/2", methods=["POST"])
# def f2():
#     number1 = request.form["inf1"]
#     number2 = request.form["inf2"]
#     sum_1 = int(number1) + int(number2)
#     factorial = cache.get(sum_1)
#     if not factorial:
#         factorial = 1
#         for i in range(1, sum_1 + 1):
#             factorial = factorial * i
#         print()
#         cache.set(sum_1, factorial)
#     return str(factorial)
#
# if __name__ == '__main__':
#     app.run(port=8000) # , debug=True
