from sample_app import app

def test_ejemplo():
    assert 1 + 1 == 2  # nosec B101

def test_home_status_code():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200  # nosec B101
