import pytest
from copy import deepcopy

from verification import calcular_horarios_saidas
from verification import MediaPercurso, Linha, Evento

from verification_demand import cria_eventos_saidas
from verification_demand import trata_demanda_percentual
from verification_demand import remove_demanda_inexistente
from verification_demand import junta_demanda
from verification_demand import soma_demanda
from verification_demand import porc_de_linha_desce_em_ponto
from verification_demand import porcentagem_chegada_por_ponto
from verification_demand import porcentagem_chegada_total
from verification_demand import porcentagem_geral_dias
from verification_demand import porcentagem_geral_dias_por_ponto
from verification_demand import distribui_pessoas
from verification_demand import calcula_atendimento_ida, calcula_atendimento_volta
from verification_demand import simula
from verification_demand import LinhaRota, Rota, Demanda, ResultadoSimulacao

def mock_linhas_rotas():
    return {
        '8012': LinhaRota(
            Linha(
                '8012',
                calcular_horarios_saidas([3]),
                MediaPercurso([(0, 30), (120, 80), (200, 10)])
            ),
            Rota(
                ['1859', '1846', '1924', '1934', '2', '1930', '1920', '1839', '1922', '1863', '1857', '1926', '1871', '1938'],
                ['1918', '1914', '1922', '1887', '1806', '1813', '1791', '1811', '1841', '1804', '1867', '1796', '1800', '1892', '1809', '1832', '1830', "7"]
            )
        ),
        '8022': LinhaRota(
            Linha(
                '8022',
                calcular_horarios_saidas([1, 2]),
                MediaPercurso([(0, 30)]),
            ),
            Rota(
                ['1861', '1865', '1924', '1899', '1934', '1904', '1', '1930', '1920', '3', '1818', '1826', '1850', '1848', '1926', '5', '6', '1802', '1928', '1910', '1932'],
                ['1834', '1890', '1940', '1908', '1922', '1932', '1791', '1844', '1896', '8', '1936', '1928', '1912', '1920', '1832']
            )
        )
    }

def mock_demandas():
    return Demanda(
        ida_butanta={
            'seg': {
                480: { 'FEA': 100, 'Raia Olímpica': 20},
                1140: {'FEA': 80, 'Raia Olímpica': 10}
            },
            'ter': {
                480: { 'FEA': 100, 'Raia Olímpica': 20},
                1140: {'FEA': 80, 'Raia Olímpica': 10}
            },
            'qua': {
                480: { 'FEA': 100, 'Raia Olímpica': 20},
                1140: {'FEA': 80, 'Raia Olímpica': 10}
            },
            'qui': {
                480: { 'FEA': 100, 'Raia Olímpica': 20},
                1140: {'FEA': 80, 'Raia Olímpica': 10}
            },
            'sex': {
                480: { 'FEA': 100, 'Raia Olímpica': 20},
                1140: {'FEA': 80, 'Raia Olímpica': 10}
            }
        },
        ida_p3={
            'seg': {
                480: {'ECA': 40, 'Acesso Vl. Indiana': 25},
                1140:{'ECA': 150, 'Acesso Vl. Indiana': 21}
            },
            'ter': {
                480: {'ECA': 40, 'Acesso Vl. Indiana': 25},
                1140:{'ECA': 150, 'Acesso Vl. Indiana': 21}
            },
            'qua': {
                480: {'ECA': 40, 'Acesso Vl. Indiana': 25},
                1140:{'ECA': 150, 'Acesso Vl. Indiana': 21}
            },
            'qui': {
                480: {'ECA': 40, 'Acesso Vl. Indiana': 25},
                1140:{'ECA': 150, 'Acesso Vl. Indiana': 21}
            },
            'sex': {
                480: {'ECA': 40, 'Acesso Vl. Indiana': 25},
                1140:{'ECA': 150, 'Acesso Vl. Indiana': 21}
            }
        },
        volta_butanta={
            'seg': {
                1110: {'Cultura Japonesa': 11, 'Portaria III': 52}
            },
            'ter': {
                1110: {'Cultura Japonesa': 11, 'Portaria III': 52}
            },
            'qua': {
                1110: {'Cultura Japonesa': 11, 'Portaria III': 52}
            },
            'qui': {
                1110: {'Cultura Japonesa': 11, 'Portaria III': 52}
            },
            'sex': {
                1110: {'Cultura Japonesa': 11, 'Portaria III': 52}
            }
        },
        volta_p3={
            'seg': {
                1110: {'História e Geografia': 34, 'IPT': 9}
            },
            'ter': {
                1110: {'História e Geografia': 34, 'IPT': 9}
            },
            'qua': {
                1110: {'História e Geografia': 34, 'IPT': 9}
            },
            'qui': {
                1110: {'História e Geografia': 34, 'IPT': 9}
            },
            'sex': {
                1110: {'História e Geografia': 34, 'IPT': 9}
            }
        }
    )

class TestCriaEventosSaidas:
    linhas_rotas = mock_linhas_rotas()
    saidas = cria_eventos_saidas(linhas_rotas)

    def test_base(self):
        expected = [Evento('8012', 0), Evento('8022', 0), Evento('8012', 20), Evento('8012', 40), Evento('8022', 60), Evento('8022', 90)]
        assert self.saidas == expected

    def test_count(self):
        expected = 6
        assert len(self.saidas) == expected

    def test_sorted(self):
        for i in range(len(self.saidas) - 1):
            assert self.saidas[i] < self.saidas[i + 1]

class TestTrataDemandaPercentual:
    demandas_separadas = mock_demandas()

    @pytest.mark.parametrize("demanda, porcentagem, expected", [
        (demandas_separadas.ida_butanta, 0.8, {'seg': {480: {'FEA': 80, 'Raia Olímpica': 16}, 1140: {'FEA': 64, 'Raia Olímpica': 8}},
                                            'ter': {480: {'FEA': 80, 'Raia Olímpica': 16}, 1140: {'FEA': 64, 'Raia Olímpica': 8}},
                                            'qua': {480: {'FEA': 80, 'Raia Olímpica': 16}, 1140: {'FEA': 64, 'Raia Olímpica': 8}},
                                            'qui': {480: {'FEA': 80, 'Raia Olímpica': 16}, 1140: {'FEA': 64, 'Raia Olímpica': 8}},
                                            'sex': {480: {'FEA': 80, 'Raia Olímpica': 16}, 1140: {'FEA': 64, 'Raia Olímpica': 8}}}),
        (demandas_separadas.volta_p3, 0.2, {'seg': {1110: {'História e Geografia': 7,'IPT': 2}},
                                            'ter': {1110: {'História e Geografia': 7,'IPT': 2}},
                                            'qua': {1110: {'História e Geografia': 7,'IPT': 2}},
                                            'qui': {1110: {'História e Geografia': 7,'IPT': 2}},
                                            'sex': {1110: {'História e Geografia': 7,'IPT': 2}}})
    ])

    def test_handle_demand_perc(self, demanda, porcentagem, expected):
        trata_demanda_percentual(demanda, porcentagem)
        assert demanda == expected

class TestRemoveDemandaInexistente:
    demandas_separadas = mock_demandas()

    @pytest.mark.parametrize("demanda, expected", [
        (demandas_separadas.ida_p3, demandas_separadas.ida_p3),
        ({'seg': {1110: {'Cultura Japonesa': 11, 'Portaria III': 52, 'ECA': {}}}}, {'seg': {1110: {'Cultura Japonesa': 11, 'Portaria III': 52}}}),
        ({'seg': {1110: {'Cultura Japonesa': {}, 'Portaria III': {}}}}, {'seg': {1110: {}}})
    ])

    def test_remove_non_existent_demanda(self, demanda, expected):
        remove_demanda_inexistente(demanda)
        assert demanda == expected

class TestJuntaDemanda:
    demandas_separadas = mock_demandas()

    @pytest.mark.parametrize("demanda1, demanda2, expected", [
        (demandas_separadas.ida_butanta, demandas_separadas.ida_p3, {'seg': {480: {'Acesso Vl. Indiana': 25, 'ECA': 40, 'FEA': 100, 'Raia Olímpica': 20}, 1140: {'Acesso Vl. Indiana': 21, 'ECA': 150, 'FEA': 80, 'Raia Olímpica': 10}},
                                                                    'ter': {480: {'Acesso Vl. Indiana': 25, 'ECA': 40, 'FEA': 100, 'Raia Olímpica': 20}, 1140: {'Acesso Vl. Indiana': 21, 'ECA': 150, 'FEA': 80, 'Raia Olímpica': 10}},
                                                                    'qua': {480: {'Acesso Vl. Indiana': 25, 'ECA': 40, 'FEA': 100, 'Raia Olímpica': 20}, 1140: {'Acesso Vl. Indiana': 21, 'ECA': 150, 'FEA': 80, 'Raia Olímpica': 10}},
                                                                    'qui': {480: {'Acesso Vl. Indiana': 25, 'ECA': 40, 'FEA': 100, 'Raia Olímpica': 20}, 1140: {'Acesso Vl. Indiana': 21, 'ECA': 150, 'FEA': 80, 'Raia Olímpica': 10}},
                                                                    'sex': {480: {'Acesso Vl. Indiana': 25, 'ECA': 40, 'FEA': 100, 'Raia Olímpica': 20}, 1140: {'Acesso Vl. Indiana': 21, 'ECA': 150, 'FEA': 80, 'Raia Olímpica': 10}}}),
        ({}, {}, {}),
        (demandas_separadas.ida_butanta, {}, demandas_separadas.ida_butanta),
    ])

    def test_join_demand(self, demanda1, demanda2, expected):  
        demanda_total = junta_demanda(demanda1, demanda2)              
        assert demanda_total == expected
    
class TestSomaDemanda:
    demandas_separadas = mock_demandas()

    @pytest.mark.parametrize("demanda, expected", [
        (demandas_separadas.ida_p3, {'seg': {480: 65, 1140: 171}, 'ter': {480: 65, 1140: 171}, 'qua': {480: 65, 1140: 171}, 'qui': {480: 65, 1140: 171}, 'sex': {480: 65, 1140: 171}}),
        (demandas_separadas.volta_butanta, {'seg': {1110: 63}, 'ter': {1110: 63}, 'qua': {1110: 63}, 'qui': {1110: 63}, 'sex': {1110: 63}}),
        ({}, {})
    ])

    def test_sum_demand(self, demanda, expected):
        demanda_soma = soma_demanda(demanda)
        assert demanda_soma == expected

class TestPorcDeLinhaDesceEmPonto:
    demandas_separadas = mock_demandas()

    @pytest.mark.parametrize("ponto_alvo, demanda, expected",[
        ("FEA", demandas_separadas.ida_butanta['seg'][480],0.8333),
        ("Ponto Inexistente", demandas_separadas.ida_p3['seg'][1140], 0),
        ("ECA", {}, 0)
    ])

    def test_perc_get_off_bus_at_stop(self, ponto_alvo, demanda, expected):
        porc_desce_ponto = porc_de_linha_desce_em_ponto(ponto_alvo, demanda)
        assert (porc_desce_ponto - expected) < 0.0001

class TestPorcentagemChegadaPorPonto:
    demandas_separadas = mock_demandas()

    @pytest.mark.parametrize("demanda_total, demanda_restante, expected", [
        (demandas_separadas.ida_butanta, demandas_separadas.ida_butanta, {'seg': {480: {'FEA': 0.0, 'Raia Olímpica': 0.0}, 1140: {'FEA': 0.0, 'Raia Olímpica': 0.0}},
                                                                        'ter': {480: {'FEA': 0.0, 'Raia Olímpica': 0.0}, 1140: {'FEA': 0.0, 'Raia Olímpica': 0.0}},
                                                                        'qua': {480: {'FEA': 0.0, 'Raia Olímpica': 0.0}, 1140: {'FEA': 0.0, 'Raia Olímpica': 0.0}},
                                                                        'qui': {480: {'FEA': 0.0, 'Raia Olímpica': 0.0}, 1140: {'FEA': 0.0, 'Raia Olímpica': 0.0}},
                                                                        'sex': {480: {'FEA': 0.0, 'Raia Olímpica': 0.0}, 1140: {'FEA': 0.0, 'Raia Olímpica': 0.0}}}),
        (demandas_separadas.ida_butanta, {'seg': {480: {'FEA': 0, 'Raia Olímpica': 0}, 1140: {'FEA': 0, 'Raia Olímpica': 0}},
                                        'ter': {480: {'FEA': 0, 'Raia Olímpica': 0}, 1140: {'FEA': 0, 'Raia Olímpica': 0}},
                                        'qua': {480: {'FEA': 0, 'Raia Olímpica': 0}, 1140: {'FEA': 0, 'Raia Olímpica': 0}},
                                        'qui': {480: {'FEA': 0, 'Raia Olímpica': 0}, 1140: {'FEA': 0, 'Raia Olímpica': 0}},
                                        'sex': {480: {'FEA': 0, 'Raia Olímpica': 0}, 1140: {'FEA': 0, 'Raia Olímpica': 0}}},
                                        {'seg': {480: {'FEA': 1.0, 'Raia Olímpica': 1.0}, 1140: {'FEA': 1.0, 'Raia Olímpica': 1.0}},
                                        'ter': {480: {'FEA': 1.0, 'Raia Olímpica': 1.0}, 1140: {'FEA': 1.0, 'Raia Olímpica': 1.0}},
                                        'qua': {480: {'FEA': 1.0, 'Raia Olímpica': 1.0}, 1140: {'FEA': 1.0, 'Raia Olímpica': 1.0}},
                                        'qui': {480: {'FEA': 1.0, 'Raia Olímpica': 1.0}, 1140: {'FEA': 1.0, 'Raia Olímpica': 1.0}},
                                        'sex': {480: {'FEA': 1.0, 'Raia Olímpica': 1.0}, 1140: {'FEA': 1.0, 'Raia Olímpica': 1.0}}}),
        (demandas_separadas.ida_butanta, {'seg': {480: {'FEA': 50, 'Raia Olímpica': 10}, 1140: {'FEA': 40, 'Raia Olímpica': 5}},
                                        'ter': {480: {'FEA': 50, 'Raia Olímpica': 10}, 1140: {'FEA': 40, 'Raia Olímpica': 5}},
                                        'qua': {480: {'FEA': 50, 'Raia Olímpica': 10}, 1140: {'FEA': 40, 'Raia Olímpica': 5}},
                                        'qui': {480: {'FEA': 50, 'Raia Olímpica': 10}, 1140: {'FEA': 40, 'Raia Olímpica': 5}},
                                        'sex': {480: {'FEA': 50, 'Raia Olímpica': 10}, 1140: {'FEA': 40, 'Raia Olímpica': 5}}},
                                        {'seg': {480: {'FEA': 0.5, 'Raia Olímpica': 0.5}, 1140: {'FEA': 0.5, 'Raia Olímpica': 0.5}},
                                        'ter': {480: {'FEA': 0.5, 'Raia Olímpica': 0.5}, 1140: {'FEA': 0.5, 'Raia Olímpica': 0.5}},
                                        'qua': {480: {'FEA': 0.5, 'Raia Olímpica': 0.5}, 1140: {'FEA': 0.5, 'Raia Olímpica': 0.5}},
                                        'qui': {480: {'FEA': 0.5, 'Raia Olímpica': 0.5}, 1140: {'FEA': 0.5, 'Raia Olímpica': 0.5}},
                                        'sex': {480: {'FEA': 0.5, 'Raia Olímpica': 0.5}, 1140: {'FEA': 0.5, 'Raia Olímpica': 0.5}}})
    ])

    def test_perc_arrival_per_stop(self, demanda_total, demanda_restante, expected):
        porc_chegada_ponto = porcentagem_chegada_por_ponto(demanda_total, demanda_restante)
        assert porc_chegada_ponto == expected

class TestPorcentagemChegadaTotal:
    @pytest.mark.parametrize("soma_total, soma_restante, expected", [
        ({'seg': {480: 65, 1140: 171}}, {'seg': {480: 65, 1140: 171}}, {'seg': {480: 0.0, 1140: 0.0}}),
        ({'seg': {480: 65, 1140: 171}}, {'seg': {480: 0, 1140: 0}}, {'seg': {480: 1.0, 1140: 1.0}}),
        ({'seg': {480: 70, 1140: 200}}, {'seg': {480: 35, 1140: 100}}, {'seg': {480: 0.5, 1140: 0.5}})
    ])

    def test_perc_total_arrival(self, soma_total, soma_restante, expected):
        porc_chegada_total = porcentagem_chegada_total(soma_total, soma_restante)
        assert porc_chegada_total == expected

class TestPorcentagemGeralDias:
    @pytest.mark.parametrize("porc_dias_horarios, expected", [
        ({'seg': {480: 0.0, 1140: 0.0}}, {480: 0.0, 1140: 0.0}),
        ({'seg': {480: 1.0, 1140: 1.0}}, {480: 1.0, 1140: 1.0}),
        ({'seg': {480: 0.5, 1140: 0.5}}, {480: 0.5, 1140: 0.5}),
        ({'seg': {480: 0.5, 1140: 0.5}, 'ter': {480: 0.4, 1140: 0.6}}, {480: 0.45, 1140: 0.55})

    ])

    def test_perc_total_mean(self, porc_dias_horarios, expected):
        porc_media_total_chegada = porcentagem_geral_dias(porc_dias_horarios)
        assert porc_media_total_chegada == expected

class TestPorcentagemGeralDiasPorPonto:
    @pytest.mark.parametrize("porc_dias_horarios, expected", [
        ({'seg': {480: {'FEA': 0.0, 'ECA': 0.0}, 1140: {'FEA': 0.0, 'ECA': 0.0}}}, {480: {'FEA': 0.0, 'ECA': 0.0}, 1140: {'FEA': 0.0, 'ECA': 0.0}}),
        ({'seg': {480: {'FEA': 0.5, 'ECA': 0.5}, 1140: {'FEA': 1.0, 'ECA': 1.0}}}, {480: {'FEA': 0.5, 'ECA': 0.5}, 1140: {'FEA': 1.0, 'ECA': 1.0}}),
        ({'seg': {480: {'FEA': 0.5, 'ECA': 0.5}, 1140: {'FEA': 1.0, 'ECA': 1.0}}, 'qua': {480: {'FEA': 0.4, 'ECA': 0.6}, 1140: {'FEA': 0.9, 'ECA': 1.0}}},  {480: {'FEA': 0.45, 'ECA': 0.55}, 1140: {'FEA': 0.95, 'ECA': 1.0}})
    ])

    def test_perc_mean_per_stop(self, porc_dias_horarios, expected):
        porc_media_chegada_ponto = porcentagem_geral_dias_por_ponto(porc_dias_horarios)
        assert porc_media_chegada_ponto == expected

class TestDistribuiPessoas:
    linhas_rotas = mock_linhas_rotas()
    demandas_separadas = mock_demandas()
    
    @pytest.mark.parametrize("linhas_rotas, demanda, id_linha, pessoas, caminho, expected", [
        (linhas_rotas, demandas_separadas.ida_p3['seg'][1140], '8012', 50, 'volta', {'ECA': 150, 'Acesso Vl. Indiana': 21}),
        (linhas_rotas, demandas_separadas.volta_butanta['seg'][1110], '8022', 50, 'volta', {'Cultura Japonesa': 11, 'Portaria III': 52}),
    ])

    def test_deliver_people(self, linhas_rotas, demanda, id_linha, pessoas, caminho, expected):
        distribui_pessoas(linhas_rotas, demanda, id_linha, pessoas, caminho)
        assert demanda != expected
    
    @pytest.mark.parametrize("linhas_rotas, demanda, id_linha, pessoas, caminho, expected", [
        (linhas_rotas, {}, '8012', 100, 'ida', {}),
    ])

    def test_empty_demand(self, linhas_rotas, demanda, id_linha, pessoas, caminho, expected):
        distribui_pessoas(linhas_rotas, demanda, id_linha, pessoas, caminho)
        assert demanda == expected

class TestCalculaAtendimento:
    @pytest.fixture()
    def saidas(self):
        return [Evento("8012", 420), Evento('8022', 1080)]
    
    def test_compute_service(self, saidas):
        linhas_rotas = mock_linhas_rotas()

        demanda_butanta_ida = mock_demandas().ida_butanta
        demanda_p3_ida = mock_demandas().ida_p3
        demanda_butanta_volta = mock_demandas().volta_butanta
        demanda_p3_volta = mock_demandas().volta_p3

        demanda_butanta_ida_expected = deepcopy(demanda_butanta_ida)
        demanda_p3_ida_expected = deepcopy(demanda_p3_ida)
        demanda_butanta_volta_expected = deepcopy(demanda_butanta_volta)
        demanda_p3_volta_expected = deepcopy(demanda_p3_volta)
        
        calcula_atendimento_ida(linhas_rotas, demanda_butanta_ida, demanda_p3_ida, saidas)
        calcula_atendimento_volta(linhas_rotas, demanda_butanta_volta, demanda_p3_volta, saidas)

        assert demanda_butanta_ida != demanda_butanta_ida_expected
        assert demanda_p3_ida != demanda_p3_ida_expected
        assert demanda_butanta_volta != demanda_butanta_volta_expected
        assert demanda_p3_volta != demanda_p3_volta_expected

class TestSimula:
    @pytest.fixture()
    def saidas(self):
        return cria_eventos_saidas(mock_linhas_rotas())
    
    def test_simulation_result(self, saidas):
        demandas_separadas = deepcopy(mock_demandas())

        demanda_ida_completa = junta_demanda(demandas_separadas.ida_butanta, demandas_separadas.ida_p3)
        total_ida = soma_demanda(demanda_ida_completa)
        calcula_atendimento_ida(mock_linhas_rotas(), demandas_separadas.ida_butanta, demandas_separadas.ida_p3, saidas)
        demanda_ida_restante = junta_demanda(demandas_separadas.ida_butanta, demandas_separadas.ida_p3)
        restante_ida = soma_demanda(demanda_ida_restante)
        porc_atendimento_ida = porcentagem_chegada_total(total_ida, restante_ida)
        porc_atendimento_ida_ponto = porcentagem_chegada_por_ponto(demanda_ida_completa, demanda_ida_restante)

        demanda_volta_completa = junta_demanda(demandas_separadas.volta_butanta, demandas_separadas.volta_p3)
        total_volta = soma_demanda(demanda_volta_completa)
        calcula_atendimento_volta(mock_linhas_rotas(), demandas_separadas.volta_butanta, demandas_separadas.volta_p3, saidas)
        demanda_volta_restante = junta_demanda(demandas_separadas.volta_butanta, demandas_separadas.volta_p3)
        restante_volta = soma_demanda(demanda_volta_restante)
        porc_atendimento_volta = porcentagem_chegada_total(total_volta, restante_volta)
        porc_atendimento_volta_ponto = porcentagem_chegada_por_ponto(demanda_volta_completa, demanda_volta_restante)

        total_ida = porcentagem_geral_dias(porc_atendimento_ida)
        expected_total_ida_manha = total_ida[min(total_ida.keys())]
        expected_total_ida_tarde = total_ida[max(total_ida.keys())]
        total_volta = porcentagem_geral_dias(porc_atendimento_volta)
        expected_total_volta_tarde = total_volta[list(total_volta.keys())[0]]

        total_ida_ponto = porcentagem_geral_dias_por_ponto(porc_atendimento_ida_ponto)
        expected_total_ida_manha_ponto = total_ida_ponto[min(total_ida_ponto.keys())]
        expected_total_ida_tarde_ponto = total_ida_ponto[max(total_ida_ponto.keys())]
        total_volta_ponto = porcentagem_geral_dias_por_ponto(porc_atendimento_volta_ponto)
        expected_total_volta_tarde_ponto = total_volta_ponto[list(total_volta_ponto.keys())[0]]

        resultado_simulacao = simula(mock_demandas(), mock_linhas_rotas())

        assert resultado_simulacao.total_ida_manha == expected_total_ida_manha
        assert resultado_simulacao.total_ida_tarde == expected_total_ida_tarde
        assert resultado_simulacao.total_volta_tarde == expected_total_volta_tarde
        assert resultado_simulacao.total_ida_manha_ponto == expected_total_ida_manha_ponto
        assert resultado_simulacao.total_ida_tarde_ponto == expected_total_ida_tarde_ponto
        assert resultado_simulacao.total_volta_tarde_ponto == expected_total_volta_tarde_ponto
    
    def test_types(self):
        resultado_simulacao = simula(mock_demandas(), mock_linhas_rotas())
        assert type(resultado_simulacao) == ResultadoSimulacao



