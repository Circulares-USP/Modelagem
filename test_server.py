import pytest

from verification import calcular_horarios_saidas
from verification import MediaPercurso, Linha

from verification_demand import Demanda, Rota, LinhaRota

from server import trata_demanda_percentual
from server import remove_demanda_inexistente
from server import remove_linha_de_demanda
from server import cria_linhas_uniforme_atual, cria_linhas_sptrans_atual
from server import cria_rotas_atual
from server import get_demanda_hoje
from server import load_demanda
from server import load_rotas_linhas

def mock_linhas_rotas():
    return {
        '8012': LinhaRota(
            Linha(
                '8012',
                calcular_horarios_saidas([1, 1, 0, 0, 0, 2, 7, 7, 7, 7, 6, 6, 7, 7, 7, 6, 6, 7, 7, 7, 7, 6, 7, 7]),
                MediaPercurso([(0, 0)])
            ),
            Rota(
                ['Metrô Butantã', 'Metalurgia', 'Mecânica', 'Portaria II', 'Hidráulica', 'Psicologia I', 'Inova USP'],
                ['Metrô Butantã', 'Metalurgia', 'Mecânica', 'Portaria II', 'Hidráulica', 'Psicologia I', 'Inova USP']
            )
        ),
        '8022': LinhaRota(
            Linha(
                '8022',
                calcular_horarios_saidas([1, 1, 0, 0, 0, 3, 5, 5, 5, 5, 4, 4, 5, 5, 5, 4, 4, 5, 5, 5, 5, 4, 5, 5]),
                MediaPercurso([(0, 0)]),
            ),
            Rota(
                ['ECA', 'Praça do Relógio', 'Psicologia II', 'Acesso CPTM I', 'Educação Física I', 'Academia de Polícia', 'Paço das Artes', 'Educação', 'CRUSP'],
                ['ECA', 'Praça do Relógio', 'Psicologia II', 'Acesso CPTM I', 'Educação Física I', 'Academia de Polícia', 'Paço das Artes', 'Educação', 'CRUSP']
            )
        ),
        '8032': LinhaRota(
            Linha(
                '8032',
                calcular_horarios_saidas([1, 1, 0, 0, 0, 3, 5, 5, 5, 5, 4, 4, 5, 5, 5, 4, 4, 5, 5, 5, 5, 4, 5, 5]),
                MediaPercurso([(0, 0)]),
            ),
            Rota(
                ['Cultura Japonesa', 'Biblioteca Brasiliana', 'Letras', 'Geociências', 'Bancos']
            )
        )
    }

def mock_demandas():
    return Demanda(
        ida_butanta={
            'seg': {
                480: {
                    'FEA': {'8012': 100},
                    'Raia Olímpica': {'8012': 20}
                },
                1140: {
                    'FEA': {'8012': 80},
                    'Raia Olímpica': {'8012': 10}
                }
            },
            'ter': {
                480: {
                    'FEA': {'8012': 100},
                    'Raia Olímpica': {'8012': 20}
                },
                1140: {
                    'FEA': {'8012': 80},
                    'Raia Olímpica': {'8012': 10}
                }
            },
            'qua': {
                480: {
                    'FEA': {'8012': 100},
                    'Raia Olímpica': {'8012': 20}
                },
                1140: {
                    'FEA': {'8012': 80},
                    'Raia Olímpica': {'8012': 10}
                }
            },
            'qui': {
                480: {
                    'FEA': {'8012': 100},
                    'Raia Olímpica': {'8012': 20}
                },
                1140: {
                    'FEA': {'8012': 80},
                    'Raia Olímpica': {'8012': 10}
                }
            },
            'sex': {
                480: {
                    'FEA': {'8012': 100},
                    'Raia Olímpica': {'8012': 20}
                },
                1140: {
                    'FEA': {'8012': 80},
                    'Raia Olímpica': {'8012': 10}
                }
            }
        },
        ida_p3={
            'seg': {
                480: {
                    'ECA': {'8022': 40},
                    'Acesso Vl. Indiana': {'8022': 25}
                },
                1140: {
                    'ECA': {'8022': 150},
                    'Acesso Vl. Indiana': {'8022': 21}
                }
            },
            'ter': {
                480: {
                    'ECA': {'8022': 40},
                    'Acesso Vl. Indiana': {'8022': 25}
                },
                1140: {
                    'ECA': {'8022': 150},
                    'Acesso Vl. Indiana': {'8022': 21}
                }
            },
            'qua': {
                480: {
                    'ECA': {'8022': 40},
                    'Acesso Vl. Indiana': {'8022': 25}
                },
                1140: {
                    'ECA': {'8022': 150},
                    'Acesso Vl. Indiana': {'8022': 21}
                }
            },
            'qui': {
                480: {
                    'ECA': {'8022': 40},
                    'Acesso Vl. Indiana': {'8022': 25}
                },
                1140: {
                    'ECA': {'8022': 150},
                    'Acesso Vl. Indiana': {'8022': 21}
                }
            },
            'sex': {
                480: {
                    'ECA': {'8022': 40},
                    'Acesso Vl. Indiana': {'8022': 25}
                },
                1140: {
                    'ECA': {'8022': 150},
                    'Acesso Vl. Indiana': {'8022': 21}
                }
            }
        },
        volta_butanta={
            'seg': {
                1110: {
                    'Cultura Japonesa': {'8012': 11},
                    'Portaria III': {'8012': 52}
                }
            },
            'ter': {
                1110: {
                    'Cultura Japonesa': {'8012': 11},
                    'Portaria III': {'8012': 52}
                }
            },
            'qua': {
                1110: {
                    'Cultura Japonesa': {'8012': 11},
                    'Portaria III': {'8012': 52}
                }
            },
            'qui': {
                1110: {
                    'Cultura Japonesa': {'8012': 11},
                    'Portaria III': {'8012': 52}
                }
            },
            'sex': {
                1110: {
                    'Cultura Japonesa': {'8012': 11},
                    'Portaria III': {'8012': 52}
                }
            }
        },
        volta_p3={
            'seg': {
                1110: {
                    'História e Geografia': {'8022': 34},
                    'IPT': {'8022': 9}
                }
            },
            'ter': {
                1110: {
                    'História e Geografia': {'8022': 34},
                    'IPT': {'8022': 9}
                }
            },
            'qua': {
                1110: {
                    'História e Geografia': {'8022': 34},
                    'IPT': {'8022': 9}
                }
            },
            'qui': {
                1110: {
                    'História e Geografia': {'8022': 34},
                    'IPT': {'8022': 9}
                }
            },
            'sex': {
                1110: {
                    'História e Geografia': {'8022': 34},
                    'IPT': {'8022': 9}
                }
            }
        }
    )

class TestTrataDemandaPercentual:
    demandas_separadas = mock_demandas()

    @pytest.mark.parametrize("demanda, porcentagem, expected", [
        (demandas_separadas.ida_butanta, 0.8, {'seg': {480: {'FEA': {'8012': 80}, 'Raia Olímpica': {'8012': 16}}, 1140: {'FEA': {'8012': 64}, 'Raia Olímpica': {'8012': 8}}},
                                            'ter': {480: {'FEA': {'8012': 80}, 'Raia Olímpica': {'8012': 16}}, 1140: {'FEA': {'8012': 64}, 'Raia Olímpica': {'8012': 8}}},
                                            'qua': {480: {'FEA': {'8012': 80}, 'Raia Olímpica': {'8012': 16}}, 1140: {'FEA': {'8012': 64}, 'Raia Olímpica': {'8012': 8}}},
                                            'qui': {480: {'FEA': {'8012': 80}, 'Raia Olímpica': {'8012': 16}}, 1140: {'FEA': {'8012': 64}, 'Raia Olímpica': {'8012': 8}}},
                                            'sex': {480: {'FEA': {'8012': 80}, 'Raia Olímpica': {'8012': 16}}, 1140: {'FEA': {'8012': 64}, 'Raia Olímpica': {'8012': 8}}}}),
        (demandas_separadas.volta_p3, 0.2, {'seg': {1110: {'História e Geografia': {'8022': 7},'IPT': {'8022': 2}}},
                                            'ter': {1110: {'História e Geografia': {'8022': 7},'IPT': {'8022': 2}}},
                                            'qua': {1110: {'História e Geografia': {'8022': 7},'IPT': {'8022': 2}}},
                                            'qui': {1110: {'História e Geografia': {'8022': 7},'IPT': {'8022': 2}}},
                                            'sex': {1110: {'História e Geografia': {'8022': 7},'IPT': {'8022': 2}}}})
    ])

    def test_handle_demand_perc(self, demanda, porcentagem, expected):
        trata_demanda_percentual(demanda, porcentagem)
        assert demanda == expected

class TestRemoveDemandaInexistente:
    demandas_separadas = mock_demandas()

    @pytest.mark.parametrize("demanda, expected", [
        (demandas_separadas.ida_p3, demandas_separadas.ida_p3),
        ({'seg': {1110: {'Cultura Japonesa': {'8012': 11}, 'Portaria III': {'8012': 52}, 'ECA': {'8012': 0}}}}, {'seg': {1110: {'Cultura Japonesa': {'8012': 11}, 'Portaria III': {'8012': 52}}}}),
        ({'seg': {1110: {'Cultura Japonesa': {}, 'Portaria III': {}}}}, {'seg': {1110: {}}}),
        ({'seg': {1110: {'Cultura Japonesa': {'8012': 0}, 'Portaria III': {'8012': 0}}}}, {'seg': {1110: {}}})
    ])

    def test_remove_non_existent_demanda(self, demanda, expected):
        remove_demanda_inexistente(demanda)
        assert demanda == expected

class TestRemoveLinhaDeDemanda:
    demandas_separadas = mock_demandas()

    @pytest.mark.parametrize("demanda, expected", [
        (demandas_separadas.ida_butanta, {'seg': {480: {'FEA': 100, 'Raia Olímpica': 20}, 1140: {'FEA': 80,'Raia Olímpica': 10}},
                                        'ter': {480: {'FEA': 100, 'Raia Olímpica': 20}, 1140: {'FEA': 80,'Raia Olímpica': 10}},
                                        'qua': {480: {'FEA': 100, 'Raia Olímpica': 20}, 1140: {'FEA': 80,'Raia Olímpica': 10}},
                                        'qui': {480: {'FEA': 100, 'Raia Olímpica': 20}, 1140: {'FEA': 80,'Raia Olímpica': 10}},
                                        'sex': {480: {'FEA': 100, 'Raia Olímpica': 20}, 1140: {'FEA': 80,'Raia Olímpica': 10}}}),
        (demandas_separadas.volta_butanta, {'seg': {1110: {'Cultura Japonesa': 11, 'Portaria III': 52}},
                                        'ter': {1110: {'Cultura Japonesa': 11, 'Portaria III': 52}},
                                        'qua': {1110: {'Cultura Japonesa': 11, 'Portaria III': 52}},
                                        'qui': {1110: {'Cultura Japonesa': 11, 'Portaria III': 52}},
                                        'sex': {1110: {'Cultura Japonesa': 11, 'Portaria III': 52}}}),
        ({}, {})
    ])

    def test_remove_line_from_demand(self, demanda, expected):
        nova_demanda = remove_linha_de_demanda(demanda)
        assert nova_demanda == expected

class TestCriaLinhasAtual:
    @pytest.mark.parametrize("linhas", [
        (cria_linhas_uniforme_atual()),
        (cria_linhas_sptrans_atual()),
    ])

    def test_all_lines(self, linhas):
        assert '8012' in linhas
        assert '8022' in linhas
        assert '8032' in linhas

    @pytest.mark.parametrize("linhas", [
        (cria_linhas_uniforme_atual()),
        (cria_linhas_sptrans_atual()),
    ])

    def test_types(self, linhas):
        for ind_linha in (['8012', '8022', '8032']):
            linha = linhas[ind_linha]

            assert linha.id == ind_linha
            assert type(linha.horarios_de_saida) == list
            assert type(linha.media) == MediaPercurso

class TestCriaRotasAtual:
    
    @pytest.fixture()
    def rotas(self):
        return cria_rotas_atual()
    
    def test_all_lines_in_routes(self, rotas):
        assert '8012' in rotas
        assert '8022' in rotas
        assert '8032' in rotas
    
    def test_type(self, rotas):
        for ind_linha in (['8012', '8022', '8032']):
            rota = rotas[ind_linha]

            assert type(rota) == Rota

class TestGetDemandaHoje:
    def test_type(self):
        demanda = get_demanda_hoje()
        assert type(demanda) == Demanda
    
class TestLoadDemanda:
    @pytest.fixture()
    def body(self):
        return {
            'demanda': {
                'seg': {
                    'ida_manha': {
                        'de_p3': {
                            'FEA': {'8012': 100},
                            'Raia Olímpica': {'8012': 20}
                        },
                        'de_butanta': {
                            'ECA': {'8022': 40},
                            'Acesso Vl. Indiana': {'8022': 25}
                        }
                    },
                    'ida_tarde': {
                        'de_p3': {
                            'FEA': {'8012': 80},
                            'Raia Olímpica': {'8012': 10}
                        },
                        'de_butanta': {
                            'ECA': {'8022': 150},
                            'Acesso Vl. Indiana': {'8022': 21}
                        }
                    },
                    'volta_tarde': {
                        'de_p3': {
                            'Cultura Japonesa': {'8012': 11},
                            'Portaria III': {'8012': 52}
                        },
                        'de_butanta': {
                            'História e Geografia': {'8022': 34},
                            'IPT': {'8022': 9}
                        }
                    }
                },
                'ter': {
                    'ida_manha': {
                        'de_p3': {
                            'FEA': {'8012': 100},
                            'Raia Olímpica': {'8012': 20}
                        },
                        'de_butanta': {
                            'ECA': {'8022': 40},
                            'Acesso Vl. Indiana': {'8022': 25}
                        }
                    },
                    'ida_tarde': {
                        'de_p3': {
                            'FEA': {'8012': 80},
                            'Raia Olímpica': {'8012': 10}
                        },
                        'de_butanta': {
                            'ECA': {'8022': 150},
                            'Acesso Vl. Indiana': {'8022': 21}
                        }
                    },
                    'volta_tarde': {
                        'de_p3': {
                            'Cultura Japonesa': {'8012': 11},
                            'Portaria III': {'8012': 52}
                        },
                        'de_butanta': {
                            'História e Geografia': {'8022': 34},
                            'IPT': {'8022': 9}
                        }
                    }
                },
                'qua': {
                    'ida_manha': {
                        'de_p3': {
                            'FEA': {'8012': 100},
                            'Raia Olímpica': {'8012': 20}
                        },
                        'de_butanta': {
                            'ECA': {'8022': 40},
                            'Acesso Vl. Indiana': {'8022': 25}
                        }
                    },
                    'ida_tarde': {
                        'de_p3': {
                            'FEA': {'8012': 80},
                            'Raia Olímpica': {'8012': 10}
                        },
                        'de_butanta': {
                            'ECA': {'8022': 150},
                            'Acesso Vl. Indiana': {'8022': 21}
                        }
                    },
                    'volta_tarde': {
                        'de_p3': {
                            'Cultura Japonesa': {'8012': 11},
                            'Portaria III': {'8012': 52}
                        },
                        'de_butanta': {
                            'História e Geografia': {'8022': 34},
                            'IPT': {'8022': 9}
                        }
                    }
                },
                'qui': {
                    'ida_manha': {
                        'de_p3': {
                            'FEA': {'8012': 100},
                            'Raia Olímpica': {'8012': 20}
                        },
                        'de_butanta': {
                            'ECA': {'8022': 40},
                            'Acesso Vl. Indiana': {'8022': 25}
                        }
                    },
                    'ida_tarde': {
                        'de_p3': {
                            'FEA': {'8012': 80},
                            'Raia Olímpica': {'8012': 10}
                        },
                        'de_butanta': {
                            'ECA': {'8022': 150},
                            'Acesso Vl. Indiana': {'8022': 21}
                        }
                    },
                    'volta_tarde': {
                        'de_p3': {
                            'Cultura Japonesa': {'8012': 11},
                            'Portaria III': {'8012': 52}
                        },
                        'de_butanta': {
                            'História e Geografia': {'8022': 34},
                            'IPT': {'8022': 9}
                        }
                    }
                },
                'sex': {
                    'ida_manha': {
                        'de_p3': {
                            'FEA': {'8012': 100},
                            'Raia Olímpica': {'8012': 20}
                        },
                        'de_butanta': {
                            'ECA': {'8022': 40},
                            'Acesso Vl. Indiana': {'8022': 25}
                        }
                    },
                    'ida_tarde': {
                        'de_p3': {
                            'FEA': {'8012': 80},
                            'Raia Olímpica': {'8012': 10}
                        },
                        'de_butanta': {
                            'ECA': {'8022': 150},
                            'Acesso Vl. Indiana': {'8022': 21}
                        }
                    },
                    'volta_tarde': {
                        'de_p3': {
                            'Cultura Japonesa': {'8012': 11},
                            'Portaria III': {'8012': 52}
                        },
                        'de_butanta': {
                            'História e Geografia': {'8022': 34},
                            'IPT': {'8022': 9}
                        }
                    }
                }
            }
        }

    def test_load_demand(self, body):
        demandas_separadas = mock_demandas()

        demanda = load_demanda(body)
        
        assert demanda.ida_butanta == demandas_separadas.ida_butanta
        assert demanda.ida_p3 == demandas_separadas.ida_p3
        assert demanda.volta_butanta == demandas_separadas.volta_butanta
        assert demanda.volta_p3 == demandas_separadas.volta_p3
    
    def test_type(self, body):
        demanda = load_demanda(body)
        assert type(demanda) == Demanda

class TestLoadRotasLinhas:
    @pytest.fixture()
    def body(self):
        return {
            "rotas": {
                "8012": {
                    "ida": ['Metrô Butantã', 'Metalurgia', 'Mecânica', 'Portaria II', 'Hidráulica', 'Psicologia I', 'Inova USP'],
                    "volta": ['Metrô Butantã', 'Metalurgia', 'Mecânica', 'Portaria II', 'Hidráulica', 'Psicologia I', 'Inova USP']
                },
                "8022": {
                    "ida": ['ECA', 'Praça do Relógio', 'Psicologia II', 'Acesso CPTM I', 'Educação Física I', 'Academia de Polícia', 'Paço das Artes', 'Educação', 'CRUSP'],
                    "volta": ['ECA', 'Praça do Relógio', 'Psicologia II', 'Acesso CPTM I', 'Educação Física I', 'Academia de Polícia', 'Paço das Artes', 'Educação', 'CRUSP']
                },
                "8032": {
                    "ida": ['Cultura Japonesa', 'Biblioteca Brasiliana', 'Letras', 'Geociências', 'Bancos']
                }
            },
            "saidas_por_hora": {
                "0": {"8012": 1, "8022": 1, "8032": 1},
                "1": {"8012": 1, "8022": 1, "8032": 1},
                "2": {"8012": 0, "8022": 0, "8032": 0},
                "3": {"8012": 0, "8022": 0, "8032": 0},
                "4": {"8012": 0, "8022": 0, "8032": 0},
                "5": {"8012": 2, "8022": 3, "8032": 3},
                "6": {"8012": 7, "8022": 5, "8032": 5},
                "7": {"8012": 7, "8022": 5, "8032": 5},
                "8": {"8012": 7, "8022": 5, "8032": 5},
                "9": {"8012": 7, "8022": 5, "8032": 5},
                "10": {"8012": 6, "8022": 4, "8032": 4},
                "11": {"8012": 6, "8022": 4, "8032": 4},
                "12": {"8012": 7, "8022": 5, "8032": 5},
                "13": {"8012": 7, "8022": 5, "8032": 5},
                "14": {"8012": 7, "8022": 5, "8032": 5},
                "15": {"8012": 6, "8022": 4, "8032": 4},
                "16": {"8012": 6, "8022": 4, "8032": 4},
                "17": {"8012": 7, "8022": 5, "8032": 5},
                "18": {"8012": 7, "8022": 5, "8032": 5},
                "19": {"8012": 7, "8022": 5, "8032": 5},
                "20": {"8012": 7, "8022": 5, "8032": 5},
                "21": {"8012": 6, "8022": 4, "8032": 4},
                "22": {"8012": 7, "8022": 5, "8032": 5},
                "23": {"8012": 7, "8022": 5, "8032": 5}
            },
        }
    
    def test_load_routes_lines(self, body):
        linhas_rotas_expected = mock_linhas_rotas()

        linhas_rotas = load_rotas_linhas(body)

        for ind_linha in (['8012', '8022', '8032']):
            linha_rota = linhas_rotas[ind_linha]
            linha_rota_expected = linhas_rotas_expected[ind_linha]
            
            assert linha_rota.linha.id == linha_rota_expected.linha.id
            assert linha_rota.linha.horarios_de_saida == linha_rota_expected.linha.horarios_de_saida
            assert linha_rota.linha.media.media_por_horario == linha_rota_expected.linha.media.media_por_horario
            assert linha_rota.rota.ida == linha_rota_expected.rota.ida
            assert linha_rota.rota.volta == linha_rota_expected.rota.volta

    def test_type(self, body):
        linhas_rotas = load_rotas_linhas(body)
        for ind_linha in (['8012', '8022', '8032']):
            linha = linhas_rotas[ind_linha]

            assert type(linha) == LinhaRota
            assert type(linha.linha) == Linha
            assert type(linha.rota) == Rota


