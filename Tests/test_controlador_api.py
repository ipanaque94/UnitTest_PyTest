import pytest
import requests_mock
from Logica.controlador_api import ApiHandler

api_handler = ApiHandler()
status_code_to_test = [400,401,402,403,404,500,502,503]

@pytest.mark.smoke
@pytest.mark.unit
def test_get_data_from_api() :
    """GET exitoso debe retornar lista de resultados"""
    with requests_mock.Mocker() as mocker:
        mocker.get('https://rickandmortyapi.com/api/character', json={"results":[1,2,3,4]})
        data = api_handler.get_data_from_api()
        assert data == [1,2,3,4]

@pytest.mark.negative
@pytest.mark.regression
@pytest.mark.parametrize("status_code", status_code_to_test)
def test_negative_status_code(status_code) :
    """Cualquier status de error debe retornar lista vacía"""
    with requests_mock.Mocker() as mocker:
        mocker.get('https://rickandmortyapi.com/api/character', status_code=status_code , json={"results":[1,2,3,4]})
        data = api_handler.get_data_from_api()
        assert data == []  