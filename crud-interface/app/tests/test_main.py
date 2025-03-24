import pytest
import sys
import os
from fastapi.testclient import TestClient

from main import app  # Import your FastAPI app

client = TestClient(app)
secret_key = "sk_test_1234567890abcdef"

def test_health_check():
    """Test if the health check endpoint returns 200."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
