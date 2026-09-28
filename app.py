from flask import Flask, jsonify, render_template, request, redirect, url_for
import json
from pymongo import MongoClient
import os

app = Flask(__name__)


# ---------------- TASK 1 ----------------

@app.route("/api")
def api():
    with open("data.json", "r") as file:
        data = json.load(file)

    return jsonify(data)


# ---------------- TASK 2 ----------------

# MongoDB Atlas connection
MONGO_URI = os.environ.get("MONGO_URI")

client = MongoClient(MONGO_URI)

db = client["flask_assignment"]
collection = db["submissions"]


# Frontend form
@app.route("/")
def home():
    return render_template("index.html")


# Form submission
@app.route("/submit", methods=["POST"])
def submit():

    try:
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()

        if not name or not email:
            raise ValueError("Name and email are required.")

        collection.insert_one({
            "name": name,
            "email": email
        })

        return redirect(url_for("success"))

    except Exception as error:

        return render_template(
            "index.html",
            error=str(error),
            name=request.form.get("name", ""),
            email=request.form.get("email", "")
        )


# Success page
@app.route("/success")
def success():
    return render_template("success.html")


# Start Flask
if __name__ == "__main__":
    app.run(debug=True)