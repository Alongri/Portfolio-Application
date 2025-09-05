import io
import pandas as pd
import pytest
import app.main as main  # import the module directly
from app.main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_post_upload(client, monkeypatch):
    """Test POST /upload/ with a small Excel file"""

    # Dummy Excel file
    df = pd.DataFrame({"Name": ["Alice", "Bob"], "Age": [30, 25]})
    excel_buffer = io.BytesIO()
    df.to_excel(excel_buffer, index=False)
    excel_buffer.seek(0)

    # Dummy DB
    class DummyCollection:
        def __init__(self):
            self.inserted = []

        def insert_many(self, data):
            self.inserted = data
            return True

    class DummyDB:
        def __init__(self):
            self.excel_data = DummyCollection()


    # Patch get_db() on the module object
    monkeypatch.setattr(main, "get_db", lambda: DummyDB())

    data = {"file": (excel_buffer, "test.xlsx")}
    response = client.post("/upload/", data=data, content_type="multipart/form-data")

    assert response.status_code == 200
    assert b"uploaded successfully" in response.data

    dummy_db_instance = main.get_db()
    assert len(dummy_db_instance.excel_data.inserted) == 2
