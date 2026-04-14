import pytest
import sys
import os

# Ensure backend module is in path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def test_integration_health(app_client):
    """
    Dummy integration test to ensure the health endpoint
    returns status correctly when the backend API is up.
    """
    response = app_client.get('/api/health')
    assert response.status_code == 200
    json_data = response.get_json()
    assert "status" in json_data
