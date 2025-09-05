from flask import Flask, request, render_template, jsonify
from pymongo import MongoClient
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "uploads"

# MongoDB client
MONGO_USER = os.getenv("ROOT_USERNAME")
MONGO_PASSWORD = os.getenv("ROOT_PASSWORD")
MONGO_DB = os.getenv("MONGO_DB")
MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))

db = None
def get_db():
    global db
    if db is None:
        # Use production Mongo if MONGO_HOST is set
        if MONGO_HOST:
            uri = f"mongodb://root:MyRootPassword123@portfolio-umbrella-mongodb-headless:27017/excel_db?authSource=admin"
            client = MongoClient(uri)
            db_name = MONGO_DB
        else:
            # Fallback to local Mongo for dev
            print("Using local MongoDB for development")
            client = MongoClient("mongodb://root:MyRootPassword123@mongo:27017")
            db_name = "excel_db"

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
    if not data:
        return {"status": "No data to insert"}, 400

    get_db().excel_data.insert_many(data)
    return {"filename": file.filename, "status": "uploaded successfully"}


# Get all data
@app.route("/data/", methods=["GET"])
def get_data():
    data = list(get_db().excel_data.find({}, {"_id": 0}))
    return jsonify({"data": data})

@app.route("/health")
def health():
    return "ok", 200

# Serve static files (CSS, JS)
app.static_folder = 'static'

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
