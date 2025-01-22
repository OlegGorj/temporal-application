import pytest
from unittest.mock import Mock, patch
from api.main import app
import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_temporal_client():
    with patch('api.main.temporal_client') as mock:
        yield mock

def test_request_endpoint_success(client, mock_temporal_client):
    # Arrange
    test_payload = {"data": "test"}
    
    # Act
    response = client.post('/request', 
                         data=json.dumps(test_payload),
                         content_type='application/json')
    
    # Assert
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "request_id" in data
    assert "callback_url" in data
    assert data["callback_url"].startswith("/request/")
    mock_temporal_client.start_workflow.assert_called_once()

def test_request_endpoint_invalid_json(client):
    # Act
    response = client.post('/request', 
                         data="invalid json",
                         content_type='application/json')
    
    # Assert
    assert response.status_code == 400

def test_request_endpoint_temporal_error(client, mock_temporal_client):
    # Arrange
    mock_temporal_client.start_workflow.side_effect = Exception("Temporal error")
    
    # Act
    response = client.post('/request', 
                         data=json.dumps({"data": "test"}),
                         content_type='application/json')
    
    # Assert
    assert response.status_code == 500