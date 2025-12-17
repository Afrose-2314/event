from flask import Flask, render_template, request, redirect
import sqlite3, time, os

app = Flask(__name__)

DB_NAME = "leaderboard.db"
start_time = {}

# ---------------- DATABASE AUTO-CREATE ----------------
def init_db():
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        score INTEGER,
        time REAL
    )
    """)
    con.commit()
    con.close()

init_db()   # 🔥 AUTO RUNS ON FIRST START

# ---------------- ROUTES ----------------

@app.route("/", methods=["GET","POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        start_time[name] = time.time()
        return redirect("/level1?name=" + name)
    return render_template("index.html")

@app.route("/level1")
def level1():
    return render_template("level1.html", name=request.args["name"])

@app.route("/level2")
def level2():
    return render_template("level2.html", name=request.args["name"])

@app.route("/submit")
def submit():
    name = request.args["name"]
    score = int(request.args["score"])

    total_time = round(time.time() - start_time[name], 2)

    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()
    cur.execute(
        "INSERT INTO scores (name, score, time) VALUES (?,?,?)",
        (name, score, total_time)
    )
    con.commit()
    con.close()

    return redirect("/leaderboard")

@app.route("/leaderboard")
def leaderboard():
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()
    cur.execute(
        "SELECT name, score, time FROM scores ORDER BY score DESC, time ASC"
    )
    data = cur.fetchall()
    con.close()
    return render_template("leaderboard.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)
