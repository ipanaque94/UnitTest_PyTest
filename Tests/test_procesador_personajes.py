import pytest
from Logica.procesador_personajes import ProcesadorPersonajes

# ============================================================
# FIXTURES
# ============================================================

@pytest.fixture
def personajes_muestra():
    """Fixture base con datos de prueba"""
    return [
        {"id": 1, "name": "Rick Sanchez",  "status": "Alive",  "species": "Human"},
        {"id": 2, "name": "Morty Smith",   "status": "Alive",  "species": "Human"},
        {"id": 3, "name": "Mr. Meeseeks",  "status": "Dead",   "species": "Alien"},
        {"id": 4, "name": "Birdperson",    "status": "Alive",  "species": "Alien"},
        {"id": 5, "name": "Beth Smith",    "status": "Alive",  "species": "Human"},
    ]

@pytest.fixture
def personajes_vacios():
    """Fixture para lista vacía"""
    return []

@pytest.fixture
def procesador(personajes_muestra):
    """Fixture dependiente — usa personajes_muestra"""
    return ProcesadorPersonajes(personajes_muestra)

@pytest.fixture
def procesador_vacio(personajes_vacios):
    """Fixture dependiente con lista vacía"""
    return ProcesadorPersonajes(personajes_vacios)

# ============================================================
# FIXTURE PARAMETRIZADO
# ============================================================

@pytest.fixture(params=[
    {"status": "Alive",  "expected_count": 4},
    {"status": "Dead",   "expected_count": 1},
    {"status": "unknown","expected_count": 0},
])
def filtro_por_status(request):
    """Fixture parametrizado para filtrar por status"""
    return request.param

# ============================================================
# TESTS — TDD: estos tests se escriben ANTES de la lógica
# ============================================================

class TestFiltrarVivos:

    @pytest.mark.smoke
    @pytest.mark.unit
    def test_filtra_personajes_vivos(self, procesador):
        """Solo deben quedar personajes con status Alive"""
        vivos = procesador.filtrar_por_status("Alive")
        assert len(vivos) == 4

    @pytest.mark.unit
    def test_filtra_personajes_muertos(self, procesador):
        """Solo deben quedar personajes con status Dead"""
        muertos = procesador.filtrar_por_status("Dead")
        assert len(muertos) == 1
        assert muertos[0]["name"] == "Mr. Meeseeks"

    @pytest.mark.unit
    def test_filtra_status_inexistente_retorna_vacio(self, procesador):
        """Status que no existe debe retornar lista vacía"""
        resultado = procesador.filtrar_por_status("unknown")
        assert resultado == []

    @pytest.mark.regression
    @pytest.mark.parametrize("status,expected", [
        ("Alive",   4),
        ("Dead",    1),
        ("unknown", 0),
    ])
    def test_filtra_por_status_parametrizado(self, procesador, status, expected):
        """Test parametrizado para múltiples status"""
        resultado = procesador.filtrar_por_status(status)
        assert len(resultado) == expected

    @pytest.mark.unit
    def test_lista_vacia_retorna_vacio(self, procesador_vacio):
        """Lista vacía debe retornar vacío"""
        resultado = procesador_vacio.filtrar_por_status("Alive")
        assert resultado == []


class TestContarHumanos:

    @pytest.mark.smoke
    @pytest.mark.unit
    def test_cuenta_humanos_correctamente(self, procesador):
        """Debe contar exactamente 3 humanos"""
        total = procesador.contar_por_especie("Human")
        assert total == 3

    @pytest.mark.unit
    def test_cuenta_aliens_correctamente(self, procesador):
        """Debe contar exactamente 2 aliens"""
        total = procesador.contar_por_especie("Alien")
        assert total == 2

    @pytest.mark.negative
    def test_especie_inexistente_retorna_cero(self, procesador):
        """Especie que no existe debe retornar 0"""
        total = procesador.contar_por_especie("Robot")
        assert total == 0

    @pytest.mark.negative
    def test_lista_vacia_retorna_cero(self, procesador_vacio):
        """Lista vacía debe retornar 0"""
        total = procesador_vacio.contar_por_especie("Human")
        assert total == 0


class TestAgruparPorEspecie:

    @pytest.mark.smoke
    @pytest.mark.unit
    def test_agrupa_por_especie(self, procesador):
        """Debe retornar dict con especies como keys"""
        grupos = procesador.agrupar_por_especie()
        assert "Human" in grupos
        assert "Alien" in grupos

    @pytest.mark.unit
    def test_grupo_human_tiene_3_personajes(self, procesador):
        """El grupo Human debe tener 3 personajes"""
        grupos = procesador.agrupar_por_especie()
        assert len(grupos["Human"]) == 3

    @pytest.mark.unit
    def test_grupo_alien_tiene_2_personajes(self, procesador):
        """El grupo Alien debe tener 2 personajes"""
        grupos = procesador.agrupar_por_especie()
        assert len(grupos["Alien"]) == 2

    @pytest.mark.unit
    def test_lista_vacia_retorna_dict_vacio(self, procesador_vacio):
        """Lista vacía debe retornar dict vacío"""
        grupos = procesador_vacio.agrupar_por_especie()
        assert grupos == {}

    @pytest.mark.regression
    def test_nombres_en_grupo_human(self, procesador):
        """Los nombres del grupo Human deben ser correctos"""
        grupos = procesador.agrupar_por_especie()
        nombres = [p["name"] for p in grupos["Human"]]
        assert "Rick Sanchez" in nombres
        assert "Morty Smith" in nombres
        assert "Beth Smith" in nombres