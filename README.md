# 🗂️ Excel Uploader SaaS Application

A modern **Python Flask-based SaaS web application** that allows users to upload Excel files, store their contents in **MongoDB**, and access the data via a REST API. The application uses **Nginx** to serve static files and reverse-proxy the Flask backend.

---

## 🚀 Features

* **Upload Excel files** (`.xlsx` and `.xls`) via a simple, stylish form
* **Store Excel data** directly in MongoDB
* **REST API endpoints** to retrieve uploaded data (`GET /data/`)
* **Stylish responsive frontend**
* **Dockerized environment** with Flask, MongoDB, and Nginx
* **.env configuration** for database credentials and app settings

---

## 🏗️ Tech Stack

| Component        | Technology/Library      |
| ---------------- | ----------------------- |
| Backend          | Python 3.11, Flask      |
| Database         | MongoDB 6               |
| Frontend         | HTML, CSS               |
| Web Server       | Nginx                   |
| Dockerized Setup | Docker & Docker Compose |
| Excel Parsing    | Pandas, openpyxl        |
| Environment Vars | python-dotenv           |

---

## 📁 Project Structure

```
saas_app/
├─ app/
│  ├─ main.py               # Flask application
│  ├─ requirements.txt      # Python dependencies
│  ├─ templates/
│  │  └─ upload.html        # Excel upload form
│  └─ static/               # CSS / JS / images
├─ nginx/
│  └─ nginx.conf            # Nginx configuration
├─ docker-compose.yml       # Docker Compose setup
└─ .env                     # Environment variables
```

---

## ⚡ Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/excel-uploader.git
cd excel-uploader
```

### 2. Create a `.env` file

```env
MONGO_INITDB_ROOT_USERNAME=admin
MONGO_INITDB_ROOT_PASSWORD=admin123
MONGO_DB=excel_db
APP_HOST=app
APP_PORT=5000
```

### 3. Build and run with Docker Compose

```bash
docker-compose up --build
```

### 4. Access the application

* Frontend form: [http://localhost/](http://localhost/)
* API endpoint: [http://localhost/data/](http://localhost/data/)

---

## 📝 Usage

1. Open the homepage and upload an Excel file.
2. The app reads the Excel file and stores it in MongoDB.
3. Retrieve uploaded data via the `/data/` GET endpoint.

---

## 🔧 Docker Compose Services

| Service | Description                          |
| ------- | ------------------------------------ |
| `mongo` | MongoDB database container           |
| `app`   | Flask application container          |
| `nginx` | Reverse proxy and static file server |

---

## 📌 Notes

* Make sure port `80` (Nginx) and `27017` (MongoDB) are free on your machine.
* Uploaded Excel files are **parsed in memory**, no local storage needed.
* The frontend is **responsive**, works on desktop and mobile.

---

## 📚 Dependencies

* Flask
* pandas
* openpyxl
* pymongo
* python-dotenv

Install locally (optional):

```bash
pip install -r app/requirements.txt
```

---

## 🌟 Future Improvements

* Add **user authentication**
* Support **Excel file validation and error messages**
* Add **success/error notifications** on the frontend
* Enable **filtering and querying** of uploaded data
* Deploy to **cloud platform** (AWS, GCP, or Azure)

---

## 🔗 Links

* Flask: [https://flask.palletsprojects.com](https://flask.palletsprojects.com)
* MongoDB: [https://www.mongodb.com](https://www.mongodb.com)
* Docker: [https://www.docker.com](https://www.docker.com)

