from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    user_input = request.form["user_input"]
    return render_template("result.html", user_input=user_input)

@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("q")
    return f"You are searching for: {query}"

if __name__ == "__main__":
    app.run(debug=True)