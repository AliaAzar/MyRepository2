from flask import Flask, render_template
from flask_caching import Cache

app = Flask(__name__)

cache = Cache(app, config={"CACHE_TYPE": "simple", "CACHE_DEFAULT_TIMEOUT": 300})

@app.route("/")
def f_1():
    return render_template("us_cache_1.html")

@app.route("/2")
def f_2():
    user_res = cache.get("us_res")
    if not user_res:
        user_res = 0
        for i in range(1000000):
            user_res += 1
        cache.set("us_res", user_res)
    return str(user_res)


