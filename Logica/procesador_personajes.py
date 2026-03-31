class ProcesadorPersonajes:
    
    def __init__(self, personajes: list):
        self.personajes = personajes

    def filtrar_por_status(self, status: str) -> list:
        """Filtra personajes por status (Alive, Dead, unknown)"""
        return [p for p in self.personajes if p["status"] == status]

    def contar_por_especie(self, especie: str) -> int:
        """Cuenta cuántos personajes son de una especie"""
        return len([p for p in self.personajes if p["species"] == especie])

    def agrupar_por_especie(self) -> dict:
        """Agrupa personajes por especie en un diccionario"""
        grupos = {}
        for personaje in self.personajes:
            especie = personaje["species"]
            if especie not in grupos:
                grupos[especie] = []
            grupos[especie].append(personaje)
        return grupos