
import os
from flask import Flask, render_template, request, make_response, session

app = Flask(__name__)

secret_key = os.environ.get("FLASK_SECRET_KEY")

if not secret_key:
    raise RuntimeError("FLASK_SECRET_KEY environment variable is required")

app.config.update(
    SECRET_KEY=secret_key,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=os.environ.get("FLASK_ENV") == "production"
)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    username = request.form.get("username", "").strip()

    if not username:
        return render_template(
            "result.html",
            user_input="",
            error="Please enter a valid username"
        )

    return render_template(
        "result.html",
        user_input=username,
        error=None
    )


@app.route("/search")
def search():
    query = request.args.get("q", "")

    return render_template("search.html", query=query)


@app.route("/set_cookie")
def set_cookie():
    response = make_response("Cookie has been set")
    response.set_cookie(
        "Username",
        "Name",
        httponly=True,
        samesite="Lax"
    )
    return response


@app.route("/set_session")
def set_session():
    session["username"] = "Mouley"
    return "Session has been set"


@app.route("/get_session")
def get_session():
    username = session.get("username")
    return f"Session username: {username}"


if __name__ == "__main__":
    app.run(debug=False)
