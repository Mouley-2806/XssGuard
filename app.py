from flask import Flask, render_template, request,make_response,session

app = Flask(__name__)
app.secret_key = "your_secret_key"  

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    username = request.form["username"]
    print(username)
    return render_template("result.html", user_input=username)

@app.route("/search")
def search():
    query = request.args.get("q")
    print("Query parameter:", query)
    response = make_response(f"You searched for: {query}")
    response.headers["X-XSSGuard-Test"] = "Day4"
    return response

@app.route("/set_cookie")
def set_cookie():
    response=make_response("Cookie has been set")
    response.set_cookie("Username", "Day4")
    return response
@app.route("/set_session")
def set_session():
    session["username"]="Mouley"
    return "session has been set"

@app.route("/get_session")
def get_cookie():
    username=session.get("username")
    return f"Session username: {username}"
    


if __name__ == "__main__":
    app.run(debug=True)