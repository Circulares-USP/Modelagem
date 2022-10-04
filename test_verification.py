from verification import calcular_horarios_saidas
from verification import cria_eventos_saidas
from verification import cria_linhas_sptrans
from verification import cria_linhas_uniforme
from verification import formata_hora
from verification import modifica_onibus_ativos
from verification import Evento, Linha, MediaPercurso

def mock_linhas():
    return {
        '8012': Linha(
            '8012',
            calcular_horarios_saidas([3]),
            MediaPercurso([(0, 30)]),
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

    def test_em(self):
        assert self.media_percurso.em(0) == 10
        assert self.media_percurso.em(4) == 10
        assert self.media_percurso.em(5) == 20
        assert self.media_percurso.em(8) == 20
        assert self.media_percurso.em(10) == 30
        assert self.media_percurso.em(50) == 50

class TestCalcularHorariosSaidas:

    def test_base(self):
        saidas = [1, 2, 3, 4, 5]
        expected = [0, 60, 90, 120, 140, 160, 180, 195, 210, 225, 240, 252, 264, 276, 288]
        horarios = calcular_horarios_saidas(saidas)
        assert horarios == expected

    def test_empty(self):
        assert calcular_horarios_saidas([]) == []

    def test_not_round(self):
        saidas = [7]
        expected = [0, 9, 17, 26, 34, 43, 51]
        horarios = calcular_horarios_saidas(saidas)
        assert horarios == expected

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

    def test_uniforme(self):
        linhas = cria_linhas_uniforme()

        assert '8012' in linhas
        assert '8022' in linhas
        assert '8032' in linhas

    def test_uniforme_types(self):

        linhas = cria_linhas_uniforme()

        for ind_linha in (['8012', '8022', '8032']):
            linha = linhas[ind_linha]

            assert linha.id == ind_linha
            assert type(linha.horarios_de_saida) == list
            assert type(linha.media) == MediaPercurso 

    def test_sptrans(self):
        linhas = cria_linhas_sptrans()

        assert '8012' in linhas
        assert '8022' in linhas
        assert '8032' in linhas

    def test_sptrans_types(self):

        linhas = cria_linhas_sptrans()

        for ind_linha in (['8012', '8022', '8032']):
            linha = linhas[ind_linha]

            assert linha.id == ind_linha
            assert type(linha.horarios_de_saida) is list
            assert type(linha.media) is MediaPercurso 

class TestFormataHora:

    def test_base(self):
        expected = "06:30"
        value = formata_hora(390)
        assert value == expected

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

   
