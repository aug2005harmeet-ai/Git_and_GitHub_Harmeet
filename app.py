from flask import Flask, jsonify, render_template, redirect, url_for, request
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


# Old form submission route
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


# ---------------- TASK 3 ----------------

# To-Do item submission API
@app.route("/submittodoitem", methods=["POST"])
def submit_todo_item():

    item_name = request.form.get("itemName", "").strip()
    item_description = request.form.get("itemDescription", "").strip()

    if not item_name or not item_description:
        return "Item Name and Item Description are required.", 400

    collection.insert_one({
        "itemName": item_name,
        "itemDescription": item_description
    })

    return "To-Do item submitted successfully!"


# Success page
@app.route("/success")
def success():
    return render_template("success.html")


# Start Flask
if __name__ == "__main__":
    app.run(debug=True)
