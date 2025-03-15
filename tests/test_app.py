from app import app

def test_get_data():
    response = app.test_client().get('/api/data')
    assert response.status_code == 200
