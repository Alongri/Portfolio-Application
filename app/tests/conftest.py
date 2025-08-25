# app/tests/conftest.py
import pytest
from dotenv import load_dotenv
import os

# Load .env file before tests
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../.env"))
