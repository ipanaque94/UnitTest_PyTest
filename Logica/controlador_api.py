# controlador_api.py
import requests

class ApiHandler:
    def get_data_from_api(self):
        response = requests.get('https://rickandmortyapi.com/api/character')
        if response.status_code == 200:
            return response.json()["results"]
        else:
            return []