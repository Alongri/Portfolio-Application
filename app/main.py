from flask import Flask, request, render_template, jsonify
from pymongo import MongoClient
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "uploads"

# MongoDB client
MONGO_USER = os.getenv("MONGO_INITDB_ROOT_USERNAME")
MONGO_PASSWORD = os.getenv("MONGO_INITDB_ROOT_PASSWORD")
MONGO_DB = os.getenv("MONGO_DB")
MONGO_HOST = os.getenv("MONGO_HOST", "mongo")

# Lazy DB initialization
db = None
def get_db():
    global db
    if db is None:
        if not all([MONGO_USER, MONGO_PASSWORD, MONGO_DB]):
            # Use a test DB in case env vars are missing
            print("Environment variables missing, using test_db")
            client = MongoClient("mongodb://localhost:27017")
            db_name = "test_db"
        else:
            client = MongoClient(f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:27017")
            db_name = MONGO_DB
        db = client[db_name]
    return db

# Home page with upload form
@app.route("/", methods=["GET"])
def index():
    return render_template("upload.html")

# Upload Excel file
@app.route("/upload/", methods=["POST"])
def upload_excel():
    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    df = pd.read_excel(file)
    data = df.to_dict(orient="records")
    get_db().excel_data.insert_many(data)

    return {"filename": file.filename, "status": "uploaded successfully"}

# Get all data
@app.route("/data/", methods=["GET"])
def get_data():
    data = list(get_db().excel_data.find({}, {"_id": 0}))
    return jsonify({"data": data})

# Serve static files (CSS, JS)
app.static_folder = 'static'

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
