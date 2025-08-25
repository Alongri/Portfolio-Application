import io
import pytest
from app.main import app, get_db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_home(client):
    """Test GET / returns 200 and contains form"""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Upload Excel File" in response.data
    assert b"type=\"file\"" in response.data

def test_post_upload(client, monkeypatch):
    """Test POST /upload/ with a small Excel file"""

    # Create a dummy Excel file in memory
    import pandas as pd
    df = pd.DataFrame({"Name": ["Alice", "Bob"], "Age": [30, 25]})
    excel_buffer = io.BytesIO()
    df.to_excel(excel_buffer, index=False)
    excel_buffer.seek(0)

    # Create a dummy DB that mimics pymongo behavior
    class DummyCollection:
        def insert_many(self, data):
            self.inserted = data
            return True

    class DummyDB:
        excel_data = DummyCollection()

    # Patch get_db() to return our dummy DB
    monkeypatch.setattr("app.main", "get_db", lambda: DummyDB())

    data = {
        "file": (excel_buffer, "test.xlsx")
    }

    response = client.post("/upload/", data=data, content_type="multipart/form-data")
    assert response.status_code == 200
    assert b"uploaded successfully" in response.data

    # Check data was "inserted" into dummy collection
    dummy_db_instance = get_db()  # returns DummyDB() due to monkeypatch
    assert len(dummy_db_instance.excel_data.inserted) == 2
