from flask import request, Flask, render_template, url_for, redirect, session, jsonify

api_key = "dfdc337a7cd778a394f0b074f56b24be"

app = Flask(__name__)
app.config["SECRET_KEY"] = "12212112"


@app.route("/")
def f_1():
    return render_template("reverse_text_api.html")

@app.route("/reverse_text")
def f_2():
    user_text = request.args.get("info1")
    reverse_user_text = user_text[::-1]
    return jsonify({"reverse_text": reverse_user_text})


if __name__ == "__main__":
    app.run(debug=True, port=8000)
