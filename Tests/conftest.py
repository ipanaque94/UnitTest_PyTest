import pytest
import requests_mock as requests_mock_module
from Logica.controlador_api import ApiHandler

@pytest.fixture(scope="session")
def api_handler():
    """Fixture de sesión — se crea una sola vez"""
    return ApiHandler()

@pytest.fixture
def mock_api_exitosa():
    """Fixture que mockea la API con respuesta exitosa"""
    with requests_mock_module.Mocker() as mocker:
        mocker.get(
            'https://rickandmortyapi.com/api/character',
            json={"results": [
                {"id": 1, "name": "Rick", "status": "Alive", "species": "Human"},
                {"id": 2, "name": "Morty", "status": "Alive", "species": "Human"},
            ]}
        )
        yield mocker

@pytest.fixture
def mock_api_fallida():
    """Fixture que mockea la API con error 500"""
    with requests_mock_module.Mocker() as mocker:
        mocker.get(
            'https://rickandmortyapi.com/api/character',
            status_code=500
        )
        yield mocker