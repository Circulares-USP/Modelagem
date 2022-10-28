import pytest
from copy import deepcopy

from verification import atrasa_saida, simula_saida
from verification import calcular_horarios_saidas
from verification import cria_eventos_saidas
from verification import cria_linhas_sptrans
from verification import cria_linhas_uniforme
from verification import formata_hora
from verification import handle_saida
from verification import modifica_onibus_ativos
from verification import verifica_chegadas
from verification import dados_por_minuto
from verification import Evento, Linha, MediaPercurso, State

def mock_linhas():
    return {
        '8012': Linha(
            '8012',
            calcular_horarios_saidas([3]),
            MediaPercurso([(0, 30), (120, 80), (200, 10)]),
        ),
        '8022': Linha(
            '8022',
            calcular_horarios_saidas([1, 2]),
            MediaPercurso([(0, 30)]),
        )
    }

class TestClassEvento:

    evento1 = Evento('8012', 0)
    evento2 = Evento('8012', 0)
    evento3 = Evento('8022', 0)
    evento4 = Evento('8022', 1)

    def test_eq(self):
        assert self.evento1 == self.evento2

    def test_lt_horario(self):
        assert self.evento3 < self.evento4

    def test_lt_linha(self):
        assert self.evento1 < self.evento3
 
class TestClassMediaPercurso:

    media_percurso = MediaPercurso([(0, 10), (5, 20), (10, 30), (15, 40), (20, 50)])

    @pytest.mark.parametrize("horario, expected", [
        (0, 10),
        (4, 10),
        (5, 20),
        (8, 20),
        (10, 30),
        (50, 50),]
    )
    def test_em(self, horario, expected):
        assert self.media_percurso.em(0) == 10
        assert self.media_percurso.em(4) == 10
        assert self.media_percurso.em(5) == 20
        assert self.media_percurso.em(8) == 20
        assert self.media_percurso.em(10) == 30
        assert self.media_percurso.em(50) == 50

class TestAtrasaSaida:

    prox_chegada = Evento("8022", 1010)

    @pytest.fixture()
    def saida(self):
        return Evento("8012", 1000)

    @pytest.fixture()
    def state(self):
        onibus_disponiveis = 10
        onibus_ativos = [(980, [3, 3, 2], 8)]
        chegadas = [Evento("8022", 1010), Evento("8012", 1050)]
        return State(onibus_disponiveis, onibus_ativos, chegadas, [], 0)

    def test_update_hora_saida(self, saida, state):
        atrasa_saida(saida, self.prox_chegada, state)
        assert saida.horario == self.prox_chegada.horario

    def test_remove_onibus_ativos(self, saida, state):
        atrasa_saida(saida, self.prox_chegada, state)
        assert state.onibus_ativos[-2] == (980, [3, 3, 2], 8)
        assert state.onibus_ativos[-1] == (1010, [3, 2, 2], 7)

    def test_remove_prox_chegada(self, saida, state):
        atrasa_saida(saida, self.prox_chegada, state)
        assert state.chegadas == [Evento("8012", 1050)]

    def test_adiciona_onibus_disponivel(self, saida, state):
        atrasa_saida(saida, self.prox_chegada, state)
        assert state.onibus_disponiveis == 11

class TestCalcularHorariosSaidas:

    @pytest.mark.parametrize("saidas, expected", [
        ([1, 2, 3, 4, 5], [0, 60, 90, 120, 140, 160, 180, 195, 210, 225, 240, 252, 264, 276, 288]),
        ([], []),
        ([7], [0, 9, 17, 26, 34, 43, 51]),]
        )
    def test_saidas(self, saidas, expected):
        assert calcular_horarios_saidas(saidas) == expected

class TestCriaEventosSaidas:

    linhas = mock_linhas()
    saidas = cria_eventos_saidas(linhas)

    def test_base(self):
        expected = [Evento('8012', 0), Evento('8022', 0), Evento('8012', 20), Evento('8012', 40), Evento('8022', 60), Evento('8022', 90)]
        assert self.saidas == expected

    def test_count(self):
        expected = 6
        assert len(self.saidas) == 6

    def test_sorted(self):
        for i in range(len(self.saidas) - 1):
            assert self.saidas[i] < self.saidas[i + 1]

class TestCriaLinhas:

    @pytest.mark.parametrize("linhas", [
        (cria_linhas_uniforme()),
        (cria_linhas_sptrans()),]
        )
    def test_all_linhas(self, linhas):
        assert '8012' in linhas
        assert '8022' in linhas
        assert '8032' in linhas

    @pytest.mark.parametrize("linhas", [
        (cria_linhas_uniforme()),
        (cria_linhas_sptrans()),]
        )
    def test_tipos(self, linhas):
        for ind_linha in (['8012', '8022', '8032']):
            linha = linhas[ind_linha]

            assert linha.id == ind_linha
            assert type(linha.horarios_de_saida) == list
            assert type(linha.media) == MediaPercurso 

class TestFormataHora:

    def test_base(self):
        expected = "06:30"
        value = formata_hora(390)
        assert value == expected

class TestHandleSaida:

    linhas = mock_linhas()

    @pytest.fixture()
    def saida(self):
        return Evento("8012", 1000)

    @pytest.fixture()
    def state(self):
        onibus_disponiveis = 10
        onibus_ativos = [(980, [3, 3, 2], 8)]
        chegadas = [Evento("8022", 1010), Evento("8012", 1050)]
        return State(onibus_disponiveis, onibus_ativos, chegadas, [], 0)

    def test_adiciona_onibus_ativos(self, saida, state):
        handle_saida(self.linhas, saida, state)
        assert state.onibus_ativos[-2] == (980, [3, 3, 2], 8)
        assert state.onibus_ativos[-1] == (1000, [4, 3, 2], 9)

    def test_remove_onibus_disponivel(self, saida, state):
        handle_saida(self.linhas, saida, state)
        assert state.onibus_disponiveis == 9

class TestModificaOnibusAtivos:

    def test_new_minute_add(self):

        num_onibus_ativos = [(0, [0, 0, 0], 0)]

        evento = Evento('8012', 10)

        modifica_onibus_ativos(num_onibus_ativos, evento, +1)
        
        assert len(num_onibus_ativos) == 2
        assert num_onibus_ativos[-1] == (10, [1, 0 ,0], 1)

    def test_new_minute_remove(self):

        num_onibus_ativos = [(10, [1, 0, 0], 1)]

        evento = Evento('8012', 20)

        modifica_onibus_ativos(num_onibus_ativos, evento, -1)
        
        assert len(num_onibus_ativos) == 2
        assert num_onibus_ativos[-1] == (20, [0, 0 ,0], 0)

    def test_same_minute_add(self):

        num_onibus_ativos = [(0, [0, 0, 0], 0)]

        evento = Evento('8012', 10)

        modifica_onibus_ativos(num_onibus_ativos, evento, +1)

        evento = Evento('8022', 10)

        modifica_onibus_ativos(num_onibus_ativos, evento, +1)
        
        assert len(num_onibus_ativos) == 2
        assert num_onibus_ativos[-1] == (10, [1, 1 ,0], 2)

    def test_same_minute_remove(self):

        num_onibus_ativos = [(10, [1, 0, 1], 2)]

        evento = Evento('8012', 20)

        modifica_onibus_ativos(num_onibus_ativos, evento, -1)

        evento = Evento('8032', 20)

        modifica_onibus_ativos(num_onibus_ativos, evento, -1)
        
        assert len(num_onibus_ativos) == 2
        assert num_onibus_ativos[-1] == (20, [0, 0 ,0], 0)

class TestVerificaChegadas:

    class Case:
        onibus_disponiveis = 14
        onibus_ativos = [(5, [1, 1, 2], 4)]

        def __init__(self, chegadas, novos_onibus, disponiveis, expected_chegadas, ativos):
            self.chegadas = chegadas
            self.expected_novos_onibus = novos_onibus
            self.expected_onibus_disponiveis = disponiveis
            self.expected_chegadas = expected_chegadas
            self.expected_onibus_ativos = ativos
            self.state = State(self.onibus_disponiveis, self.onibus_ativos, chegadas, [], 0)

        def copy(self): 
            return TestVerificaChegadas.Case(deepcopy(self.chegadas),
                        self.expected_novos_onibus,
                        self.expected_onibus_disponiveis,
                        deepcopy(self.expected_chegadas),
                        deepcopy(self.expected_onibus_ativos))

    test_case0 = Case([Evento('8032', 10), Evento('8022', 20), Evento('8012', 30), Evento('8032', 40)],
                        2,
                        16,
                        [Evento('8012', 30), Evento('8032', 40)],
                        [(5, [1, 1, 2], 4), (10, [1, 1, 1], 3), (20, [1, 0, 1], 2)])

    test_case1 = Case([],
                        0,
                        14,
                        [],
                        [(5, [1, 1, 2], 4)])

    test_case2 = Case([Evento('8012', 30), Evento('8032', 40)],
                        0,
                        14,
                        [Evento('8012', 30), Evento('8032', 40)],
                        [(5, [1, 1, 2], 4)])

    test_case3 = Case([Evento('8032', 10), Evento('8022', 20)],
                        2,
                        16,
                        [],
                        [(5, [1, 1, 2], 4), (10, [1, 1, 1], 3), (20, [1, 0, 1], 2)])

    test_cases =[
        (deepcopy(test_case0)),
        (deepcopy(test_case1)),
        (deepcopy(test_case2)),
        (deepcopy(test_case3))]

    @pytest.mark.parametrize("case_instance", deepcopy(test_cases))
    def test_calcula_novos_onibus(self, case_instance):
        assert verifica_chegadas(25, case_instance.state) == case_instance.expected_novos_onibus

    @pytest.mark.parametrize("case_instance", deepcopy(test_cases))
    def test_adiciona_novos_onibus(self, case_instance):
        verifica_chegadas(25, case_instance.state)
        assert case_instance.state.onibus_disponiveis == case_instance.expected_onibus_disponiveis

    @pytest.mark.parametrize("case_instance", deepcopy(test_cases))
    def test_remove_chegadas_anteriores(self, case_instance):
        verifica_chegadas(25, case_instance.state)
        assert case_instance.state.chegadas == case_instance.expected_chegadas

    @pytest.mark.parametrize("case_instance", deepcopy(test_cases))
    def test_modifica_onibus_ativos(self, case_instance):
        verifica_chegadas(25, case_instance.state)
        assert case_instance.state.onibus_ativos == case_instance.expected_onibus_ativos

class TestSimulaSaidas:
    class Case:
        def __init__(self, initial_state, expected_state, saida, aceita_erros, atraso_permitido):
            self.initial_state=initial_state
            self.expected_state=expected_state
            self.linhas=cria_linhas_sptrans()
            self.saida=saida
            self.aceita_erros=aceita_erros
            self.atraso_permitido=atraso_permitido

    @pytest.mark.parametrize("case", [
        Case(
            State(18, [(0, [0, 0, 0], 0)], [], [], 0),
            State(17, [(0, [0, 0, 0], 0), (30, [0, 1, 0], 1)], [Evento('8022', 30 + 67)], [], 30),
            Evento('8022', 30),
            False, 0,
        ),
        Case(
            State(0, [(630, [5, 2, 3], 10)], [Evento('8022', 638), Evento('8032', 640)], [], 630),
            State(0, [(630, [5, 2, 3], 10), (638, [6, 1, 3], 10)], [Evento('8032', 640), Evento('8012', 638 + 64)], [], 638),
            Evento('8012', 635),
            False, 0,
        ),
        Case(
            State(0, [(200, [5, 2, 3], 10)], [Evento('8022', 60*8 + 6)], [], 200),
            State(0, [(200, [5, 2, 3], 10), (60*8 + 6, [5, 1, 4], 10)], [Evento('8032', 60*8 + 6 + 35)], [60*7 + 55], 60*8 + 6),
            Evento('8032', 60*7 + 55),
            False, 10,
        ),
        Case(
            State(0, [(200, [5, 2, 3], 10)], [Evento('8022', 60*8 + 6)], [], 200),
            State(0, [(200, [5, 2, 3], 10)], [Evento('8022', 60*8 + 6)], [60*7 + 55], 200),
            Evento('8032', 60*7 + 55),
            True, 10,
        ),
        ])
    def test_state(self, case):
        simula_saida(case.initial_state, case.linhas, case.saida, case.aceita_erros, case.atraso_permitido)
        print(case.initial_state.onibus_ativos)
        print(case.expected_state.onibus_ativos)
        assert case.initial_state == case.expected_state

class TestDadosPorMinuto:
    def test_func(self):
        dados = [
            (0, [0,0,0], 0),
            (4, [0,3,1], 4),
            (7, [1,0,0], 1),
        ]
        expected = [
            (0, [0,0,0], 0),
            (1, [0,0,0], 0),
            (2, [0,0,0], 0),
            (3, [0,0,0], 0),
            (4, [0,3,1], 4),
            (5, [0,3,1], 4),
            (6, [0,3,1], 4),
            (7, [1,0,0], 1),
            (8, [1,0,0], 1),
            (9, [1,0,0], 1),
            (10, [1,0,0], 1),
        ]
        got = dados_por_minuto(dados)
        assert len(got) == 60*24
        assert got[:11] == expected
