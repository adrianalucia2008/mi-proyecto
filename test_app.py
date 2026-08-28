import pytest
from sample_app import app  # Asegúrate de importar la instancia de tu app de Flask

@pytest.fixture
def client():
    """Configura el cliente de pruebas de Flask."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_status_code(client):
    """Verifica que la ruta raíz responda con un código HTTP 200 OK."""
    response = client.get('/')
    assert response.status_code == 200

def test_version_endpoint(client):
    """Verifica que la ruta /version responda con un código HTTP 200 Ok."""
    response = client.get('/version')
    assert response.status_code == 200