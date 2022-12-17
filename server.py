from fastapi import FastAPI
from typing import Dict, Any
from verification_demand import LinhaRota, Demanda, Rota, simula, junta_demanda, id_to_nome, id_to_nome_to_list
from verification import MediaPercurso, Linha, calcular_horarios_saidas

from demanda.demanda_ida_butanta_alunos import demanda_ida_butanta_alunos
from demanda.demanda_ida_butanta_func import demanda_ida_butanta_func
from demanda.demanda_ida_p3_alunos import demanda_ida_p3_alunos
from demanda.demanda_ida_p3_func import demanda_ida_p3_func
from demanda.demanda_volta_butanta_alunos import demanda_volta_butanta_alunos
from demanda.demanda_volta_p3_alunos import demanda_volta_p3_alunos

app = FastAPI()

@app.post("/")
async def simulate_buses(body: Dict[Any, Any]):
    rotas_linhas = load_rotas_linhas(body)
    demanda = load_demanda(body)
    resultado = simula(demanda, rotas_linhas)

    # média de porcentagens da demanda total entregue e por ponto
    return {
        'totais': {
            'ida-manha': resultado.total_ida_manha,
            'ida-tarde': resultado.total_ida_tarde,
            'volta-tarde': resultado.total_volta_tarde,
        },
        'media-por-ponto': {
            'ida-manha': resultado. total_ida_manha_ponto,
            'ida-tarde': resultado.total_ida_tarde_ponto,
            'volta-tarde': resultado.total_volta_tarde_ponto,
        }
    }

@app.post("/bus_stops")
async def get_bus_stops():
    lista_pontos = id_to_nome_to_list()

    return {
        'pontos': lista_pontos,
    }

# body

def load_rotas_linhas(body):
    if 'rotas' in body:
        rotas_body = body['rotas']
        map_rotas = {}
        for id_linha in rotas_body:
            ida = rotas_body[id_linha]['ida']
            if 'volta' in rotas_body[id_linha]:
                rota = Rota(ida, rotas_body[id_linha]['volta'])
            else:
                rota = Rota(ida)
            map_rotas[id_linha] = rota
    else:
        map_rotas = cria_rotas_atual()
    
    if 'saidas_por_hora' in body:
        map_saidas_linhas = {}
        for id_linha in map_rotas:
            map_saidas_linhas[id_linha] = []

        saidas_por_hora = body['saidas_por_hora']
        for i in range(0,24):
            if str(i) not in saidas_por_hora:
                for id_linha in map_rotas:
                    map_saidas_linhas[id_linha].append(0)
            else:
                saidas_por_linha = saidas_por_hora[str(i)]
                for id_linha in saidas_por_linha:
                    map_saidas_linhas[id_linha].append(saidas_por_linha[id_linha])

        map_linhas = {}
        for id_linha in map_saidas_linhas:
            map_linhas[id_linha] = Linha(
                id_linha,
                calcular_horarios_saidas(map_saidas_linhas[id_linha]),
                MediaPercurso([(0, 0)]) # TODO: adicionar tempo de trajeto
            )
    else:
        map_linhas = cria_linhas_sptrans_atual()
    
    if sorted(list(map_rotas.keys())) != sorted(list(map_linhas.keys())):
        raise ValueError('ID das linhas em rotas e saidas_por_hora devem ser os mesmos')
    
    linhas_rotas = {}
    for id_linha in map_linhas:
        linhas_rotas[id_linha] = LinhaRota(map_linhas[id_linha], map_rotas[id_linha])
    return linhas_rotas


def load_demanda(body):
    if 'demanda' not in body:
        return get_demanda_hoje()

    body_demanda = body['demanda']
    demanda_ida_manha_p3 = body_demanda['ida_manha']['de_p3']
    demanda_ida_manha_butanta = body_demanda['ida_manha']['de_butanta']
    demanda_ida_tarde_butanta = body_demanda['ida_tarde']['de_p3']
    demanda_ida_tarde_p3 = body_demanda['ida_tarde']['de_butanta']
    demanda_volta_tarde_butanta = body_demanda['volta_tarde']['de_p3']
    demanda_volta_tarde_p3 = body_demanda['volta_tarde']['de_butanta']

    horario_manha = 480
    horario_ida_tarde = 1140
    horario_volta_tarde = 1110
    demanda_semana_ida_butanta = copia_para_todos_dias({
        horario_manha: depara_ids_pontos(demanda_ida_manha_butanta),
        horario_ida_tarde: depara_ids_pontos(demanda_ida_tarde_butanta),
    })
    demanda_semana_ida_p3 = copia_para_todos_dias({
        horario_manha: depara_ids_pontos(demanda_ida_manha_p3),
        horario_ida_tarde: depara_ids_pontos(demanda_ida_tarde_p3),
    })
    demanda_semana_volta_butanta = copia_para_todos_dias({
        horario_volta_tarde: depara_ids_pontos(demanda_volta_tarde_butanta),
    })
    demanda_semana_volta_p3 = copia_para_todos_dias({
        horario_volta_tarde: depara_ids_pontos(demanda_volta_tarde_p3),
    })

    demanda = Demanda(demanda_semana_ida_butanta, demanda_semana_ida_p3, demanda_semana_volta_butanta, demanda_semana_volta_p3)
    return demanda

def depara_ids_pontos(pontos_demanda):
    map = {}
    for id_ponto in pontos_demanda:
        map[id_to_nome[id_ponto]] = pontos_demanda[id_ponto]
    return map

def copia_para_todos_dias(dia):
    dias = ['seg','ter','qua','qui','sex']
    map = {}
    for dia_str in dias:
        map[dia_str] = dia
    return map

# demanda

def get_demanda_hoje():
    trata_demanda_percentual(demanda_ida_butanta_alunos, 0.8)
    trata_demanda_percentual(demanda_ida_butanta_func, 0.8)
    trata_demanda_percentual(demanda_volta_butanta_alunos, 0.8)
    trata_demanda_percentual(demanda_ida_p3_alunos, 0.2)
    trata_demanda_percentual(demanda_ida_p3_func, 0.2)
    trata_demanda_percentual(demanda_volta_p3_alunos, 0.2)

    remove_demanda_inexistente(demanda_ida_butanta_alunos)
    remove_demanda_inexistente(demanda_ida_butanta_func)
    remove_demanda_inexistente(demanda_volta_butanta_alunos)
    remove_demanda_inexistente(demanda_ida_p3_alunos)
    remove_demanda_inexistente(demanda_ida_p3_func)
    remove_demanda_inexistente(demanda_volta_p3_alunos)

    demanda_ida_completa_butanta = junta_demanda(demanda_ida_butanta_alunos, demanda_ida_butanta_func)
    demanda_ida_completa_p3 = junta_demanda(demanda_ida_p3_alunos, demanda_ida_p3_func)

    demanda = Demanda(demanda_ida_completa_butanta, demanda_ida_completa_p3, demanda_volta_butanta_alunos, demanda_volta_p3_alunos)
    return demanda

def trata_demanda_percentual(demanda, porc):
    for dia in demanda:
        for horario in demanda[dia]:
            for ponto in demanda[dia][horario]:
                for linha in demanda[dia][horario][ponto]:
                    demanda[dia][horario][ponto][linha] = round(demanda[dia][horario][ponto][linha] * porc)

def remove_demanda_inexistente(demanda):
    for dia in demanda:
        for horario in demanda[dia]:
            lista_pontos = []
            for ponto in demanda[dia][horario]:
                lista_linhas = []
                for linha in demanda[dia][horario][ponto]:
                    if demanda[dia][horario][ponto][linha] == 0:
                        lista_linhas.append(linha)
                for linha in lista_linhas:
                    del demanda[dia][horario][ponto][linha]
                if demanda[dia][horario][ponto] == {}:
                    lista_pontos.append(ponto)
            for ponto in lista_pontos:
                del demanda[dia][horario][ponto]

# linhas

def cria_linhas_uniforme_atual():
    return {
        '8012': Linha(
            '8012',
            calcular_horarios_saidas([ 2, 1, 1, 1, 3, 5, 7, 7, 6, 6, 5, 4, 5, 7, 7, 6, 7, 6, 7, 6, 4, 5, 6, 5 ]),
            MediaPercurso([(0, 64), (6*60, 63), (10*60, 64), (15*60, 67), (21*60, 64)])
        ),
        '8022': Linha(
            '8022',
            calcular_horarios_saidas([ 3, 3, 2, 1, 3, 5, 9, 9, 7, 6, 5, 6, 8, 6, 6, 7, 7, 7, 7, 8, 6, 5, 6, 4 ]),
            MediaPercurso([(0, 67), (6*60, 67), (10*60, 67), (15*60, 68), (21*60, 67)])
        ),
        '8032': Linha(
            '8032',
            calcular_horarios_saidas([ 2, 0, 0, 0, 0, 4, 5, 4, 5, 4, 3, 3, 4, 5, 3, 3, 4, 5, 5, 5, 3, 3, 4, 3 ]),
            MediaPercurso([(0, 32), (6*60, 35), (10*60, 32), (15*60, 33), (21*60, 32)])
        ),
    }

def cria_linhas_sptrans_atual():
    return {
        '8012': Linha(
            '8012',
            [0*60 + 15, 0*60 + 35, 1*60 + 25, 2*60 + 8, 3*60 + 10, 4*60 + 00, 4*60 + 30, 4*60 + 55, 5*60 + 10, 5*60 + 20, 5*60 + 29, 5*60 + 39, 5*60 + 50, 6*60 + 00, 6*60 + 8, 6*60 + 17, 6*60 + 26, 6*60 + 34, 6*60 + 43, 6*60 + 52, 7*60 + 00, 7*60 + 9, 7*60 + 18, 7*60 + 27, 7*60 + 36, 7*60 + 45, 7*60 + 54, 8*60 + 4, 8*60 + 14, 8*60 + 24, 8*60 + 34, 8*60 + 44, 8*60 + 55, 9*60 + 6, 9*60 + 16, 9*60 + 26, 9*60 + 37, 9*60 + 48, 9*60 + 58, 10*60 + 8, 10*60 + 18, 10*60 + 28, 10*60 + 41, 10*60 + 54, 11*60 + 7, 11*60 + 20, 11*60 + 34, 11*60 + 49, 12*60 + 2, 12*60 + 15, 12*60 + 27, 12*60 + 39, 12*60 + 51, 13*60 + 3, 13*60 + 12, 13*60 + 20, 13*60 + 29, 13*60 + 38, 13*60 + 45, 13*60 + 54, 14*60 + 2, 14*60 + 11, 14*60 + 21, 14*60 + 30, 14*60 + 37, 14*60 + 44, 14*60 + 54, 15*60 + 5, 15*60 + 15, 15*60 + 25, 15*60 + 35, 15*60 + 44, 15*60 + 52, 16*60 + 00, 16*60 + 8, 16*60 + 17, 16*60 + 27, 16*60 + 37, 16*60 + 46, 16*60 + 54, 17*60 + 2, 17*60 + 10, 17*60 + 19, 17*60 + 29, 17*60 + 40, 17*60 + 51, 18*60 + 1, 18*60 + 11, 18*60 + 20, 18*60 + 29, 18*60 + 38, 18*60 + 47, 18*60 + 56, 19*60 + 5, 19*60 + 14, 19*60 + 23, 19*60 + 32, 19*60 + 41, 19*60 + 50, 20*60 + 5, 20*60 + 20, 20*60 + 35, 20*60 + 50, 21*60 + 4, 21*60 + 18, 21*60 + 31, 21*60 + 43, 21*60 + 55, 22*60 + 5, 22*60 + 15, 22*60 + 25, 22*60 + 35, 22*60 + 45, 22*60 + 55, 23*60 + 10, 23*60 + 25, 23*60 + 40, 23*60 + 47, 23*60 + 55],
            MediaPercurso([(0, 64), (7*60, 63), (10*60, 64), (17*60, 67), (20*60, 64)])
        ),
        '8022': Linha(
            '8022',
            [0*60 + 15, 0*60 + 34, 0*60 + 52, 1*60 + 11, 1*60 + 36, 2*60 + 23, 3*60 + 15, 4*60 + 5, 4*60 + 30, 4*60 + 55, 5*60 + 10, 5*60 + 24, 5*60 + 33, 5*60 + 42, 5*60 + 51, 6*60 + 0, 6*60 + 6, 6*60 + 15, 6*60 + 24, 6*60 + 32, 6*60 + 39, 6*60 + 46, 6*60 + 52, 6*60 + 58, 7*60 + 5, 7*60 + 12, 7*60 + 18, 7*60 + 24, 7*60 + 32, 7*60 + 40, 7*60 + 47, 7*60 + 54, 7*60 + 59, 8*60 + 9, 8*60 + 19, 8*60 + 28, 8*60 + 37, 8*60 + 45, 8*60 + 53, 9*60 + 1, 9*60 + 9, 9*60 + 17, 9*60 + 26, 9*60 + 35, 9*60 + 44, 9*60 + 54, 10*60 + 4, 10*60 + 13, 10*60 + 23, 10*60 + 33, 10*60 + 42, 10*60 + 50, 11*60 + 0, 11*60 + 10, 11*60 + 20, 11*60 + 29, 11*60 + 39, 11*60 + 50, 12*60 + 0, 12*60 + 7, 12*60 + 14, 12*60 + 21, 12*60 + 29, 12*60 + 37, 12*60 + 46, 12*60 + 56, 13*60 + 7, 13*60 + 18, 13*60 + 31, 13*60 + 43, 13*60 + 54, 14*60 + 3, 14*60 + 10, 14*60 + 17, 14*60 + 25, 14*60 + 33, 14*60 + 42, 14*60 + 50, 14*60 + 57, 15*60 + 5, 15*60 + 12, 15*60 + 19, 15*60 + 27, 15*60 + 33, 15*60 + 41, 15*60 + 49, 15*60 + 57, 16*60 + 3, 16*60 + 10, 16*60 + 17, 16*60 + 24, 16*60 + 32, 16*60 + 41, 16*60 + 50, 16*60 + 58, 17*60 + 5, 17*60 + 12, 17*60 + 20, 17*60 + 28, 17*60 + 36, 17*60 + 44, 17*60 + 53, 18*60 + 3, 18*60 + 12, 18*60 + 21, 18*60 + 31, 18*60 + 42, 18*60 + 53, 19*60 + 2, 19*60 + 12, 19*60 + 22, 19*60 + 32, 19*60 + 41, 19*60 + 50, 19*60 + 58, 20*60 + 8, 20*60 + 18, 20*60 + 25, 20*60 + 33, 20*60 + 43, 20*60 + 54, 21*60 + 6, 21*60 + 17, 21*60 + 27, 21*60 + 38, 21*60 + 50, 22*60 + 1, 22*60 + 12, 22*60 + 22, 22*60 + 31, 22*60 + 41, 22*60 + 53, 23*60 + 9, 23*60 + 29, 23*60 + 43, 23*60 + 57],
            MediaPercurso([(0, 67), (7*60, 67), (10*60, 67), (17*60, 68), (20*60, 67)])
        ),
        '8032': Linha(
            '8032',
            [0*60 + 15, 0*60 + 40, 5*60 + 0, 5*60 + 30, 6*60 + 5, 6*60 + 17, 6*60 + 29, 6*60 + 41, 6*60 + 53, 7*60 + 5, 7*60 + 17, 7*60 + 29, 7*60 + 41, 7*60 + 53, 8*60 + 8, 8*60 + 23, 8*60 + 38, 8*60 + 53, 9*60 + 8, 9*60 + 23, 9*60 + 38, 9*60 + 53, 10*60 + 8, 10*60 + 23, 10*60 + 38, 10*60 + 53, 11*60 + 8, 11*60 + 23, 11*60 + 38, 11*60 + 53, 12*60 + 3, 12*60 + 13, 12*60 + 23, 12*60 + 33, 12*60 + 43, 12*60 + 53, 13*60 + 5, 13*60 + 16, 13*60 + 27, 13*60 + 38, 13*60 + 49, 14*60 + 3, 14*60 + 17, 14*60 + 34, 14*60 + 53, 15*60 + 8, 15*60 + 23, 15*60 + 40, 15*60 + 55, 16*60 + 6, 16*60 + 17, 16*60 + 29, 16*60 + 41, 16*60 + 53, 17*60 + 4, 17*60 + 16, 17*60 + 28, 17*60 + 39, 17*60 + 51, 18*60 + 3, 18*60 + 14, 18*60 + 25, 18*60 + 36, 18*60 + 47, 18*60 + 57, 19*60 + 7, 19*60 + 18, 19*60 + 29, 19*60 + 40, 19*60 + 50, 20*60 + 5, 20*60 + 20, 20*60 + 35, 20*60 + 50, 21*60 + 6, 21*60 + 22, 21*60 + 38, 21*60 + 54, 22*60 + 4, 22*60 + 14, 22*60 + 24, 22*60 + 34, 22*60 + 44, 22*60 + 54, 23*60 + 6, 23*60 + 41],
            MediaPercurso([(0, 32), (7*60, 35), (10*60, 32), (17*60, 33), (20*60, 32)])
        ),
    }

def cria_rotas_atual():
    return {
        '8012': Rota(
            ['1859', '1846', '1924', '1934', '2', '1930', '1920', '1839', '1922', '1863', '1857', '1926', '1871', '1938'],
            ['1918', '1914', '1922', '1887', '1806', '1813', '1791', '1811', '1841', '1804', '1867', '1796', '1800', '1892', '1809', '1832', '1830', "7"]
        ),
        '8022': Rota(
            ['1861', '1865', '1924', '1899', '1934', '1904', '1', '1930', '1920', '3', '1818', '1826', '1850', '1848', '1926', '5', '6', '1802', '1928', '1910', '1932'],
            ['1834', '1890', '1940', '1908', '1922', '1932', '1791', '1844', '1896', '8', '1936', '1928', '1912', '1920', '1832']
        ),
        '8032': Rota (
            ['1859', '1813', '1846', '1841', '1839', '1863', '1857', '1796', '1867', '1800', "7", "1830", "1832"]
        ),
    }
