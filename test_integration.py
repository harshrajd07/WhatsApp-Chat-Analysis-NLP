import pytest
from app import app as flask_app

@pytest.fixture
def app():
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

def test_index_page(client):
    """Test the index page."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Upload your chat file' in response.data

def test_invalid_file_upload(client):
    """Test uploading an invalid file."""
    response = client.post('/', data={'file': (b'test', 'invalid.txt')})
    assert response.status_code == 200
    assert b'An error occurred during processing' in response.data

def test_valid_file_upload(client):
    """Test uploading a valid file."""
    with open('test_data/valid_chat_file.txt', 'rb') as f:
        response = client.post('/', data={'file': (f, 'valid_chat_file.txt')})
    assert response.status_code == 200
    assert b'Upload your chat file' not in response.data

def test_get_heatmap(client):
    """Test accessing the heatmap image."""
    response = client.get('/get_heatmap')
    assert response.status_code == 200
    assert response.content_type == 'image/png'

def test_download_image(client):
    """Test downloading an image."""
    response = client.get('/download_image/activity_heatmap.png')
    assert response.status_code == 200
    assert response.content_type == 'image/png'
    assert 'attachment' in response.headers['Content-Disposition']

def test_activity_percentage(client):
    """Test activity percentage."""
    response = client.post('/activity_percentage', data={'user': 'test_user', 'activity': 'test_activity'})
    assert response.status_code == 200
    assert b'DataFrame is not loaded yet' in response.data  # Assuming the DataFrame is not loaded initially

def test_invalid_activity_percentage_input(client):
    """Test activity percentage with invalid input."""
    response = client.post('/activity_percentage', data={'user': '', 'activity': ''})
    assert response.status_code == 200
    assert b'DataFrame is not loaded yet' in response.data  # Assuming the DataFrame is not loaded initially

def test_get_nonexistent_static_file(client):
    """Test accessing a nonexistent static file."""
    response = client.get('/static/nonexistent_file.txt')
    assert response.status_code == 404

def test_invalid_route(client):
    """Test accessing an invalid route."""
    response = client.get('/invalid_route')
    assert response.status_code == 404

def test_missing_file_field(client):
    """Test uploading without a file field."""
    response = client.post('/')
    assert response.status_code == 200
    assert b'No file part' in response.data

def test_empty_file_upload(client):
    """Test uploading an empty file."""
    with open('test_data/empty_file.txt', 'rb') as f:
        response = client.post('/', data={'file': (f, 'empty_file.txt')})
    assert response.status_code == 200
    assert b'No messages found in the file' in response.data

# Add more test cases as needed for other endpoints and functionalities
