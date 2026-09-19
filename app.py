from flask import Flask, render_template, request,make_response

app = Flask(__name__)

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


if __name__ == "__main__":
    app.run(debug=True)