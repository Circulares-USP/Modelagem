from bisect import insort, bisect_left
from pprint import pprint
#import matplotlib.pyplot as plt
import sys
from verification import calcular_horarios_saidas
from verification import verifica_chegadas
from verification import handle_saida
from verification import Evento, Linha, MediaPercurso
from demanda_ida_butanta import demanda_ida_butanta
from demanda_ida_butanta_func import demanda_ida_butanta_func
from demanda_ida_p3 import demanda_ida_p3
from demanda_ida_p3_func import demanda_ida_p3_func
from demanda_volta_butanta import demanda_volta_butanta
from demanda_volta_p3 import demanda_volta_p3
from copy import deepcopy

class LinhaRota():
    def __init__(self, linha, rota):
        self.linha = linha
        self.rota = rota

class Rota():
    def __init__(self, ida, volta=None):
        self.ida = ida
        self.volta = volta
        
id_to_nome = {
    "1791": "Metrô Butantã",
    "1796": "Poli Metalúrgica",
    "1800": "Poli Mecânica",
    "1802": "Portaria II",
    "1804": "Hidráulica",
    "1806": "Psicologia I",
    "1809": "Barracões",
    "1811": "ECA",
    "1813": "Praça do Relógio",
    "1818": "Psicologia II",
    "1826": "Acesso CPTM I",
    "1830": "Escola de Educação Física I", 
    "1832": "Academia de Polícia",
    "1834": "Paços das Artes",
    "1839": "Educação",
    "1841": "CRUSP",
    "1844": "Cultura Japonesa",
    "1846": "Biblioteca Brasiliana",
    "1848": "Letras",
    "1850": "Geociências Gualberto",
    "1857": "Reitoria/Bancos",
    "1859": "FEA",
    "1861": "FAU II",
    "1863": "Poli Biênio",
    "1865": "Poli Eletrotécnica",
    "1867": "Poli Civil",
    "1871": "Cocesp I",
    "1887": "Ponto Clube dos Funcionários",
    "1890": "Física",
    "1892": "IAG",
    "1896": "Butantan",
    "1899": "Biblioteca Farmácia e Química",
    "1904": "História e Geografia",
    "1908": "CEPAM",
    "1910": "Rua do Lago",
    "1912": "Geociências I",
    "1914": "Geociências II",
    "1918": "FAU I",
    "1920": "Parada Matemática",
    "1922": "Acesso Vl. Indiana",
    "1924": "Portaria III",
    "1926": "Odontologia",
    "1928": "IPEN",
    "1930": "Biomédicas III",
    "1932": "COPESP",
    "1934": "Hospital Universitário",
    "1936": "Acesso Rio Pequeno",
    "1938": "MAE",
    "1940": "Cocesp II",
    "1": "Raia Olímpica",
    "2": "Reitoria",
    "3": "EEFE II",
    "4": "Geociências",
    "5": "Terminal USP",
    "6": "IPT",
    "7": "Acesso CPTM II",
    "8": "Oceanográfico"
}

def cria_eventos_saidas(linhas_rotas):
    saidas = []
    for id, linha_rota in linhas_rotas.items():
        saidas += list(map(lambda n: Evento(id, n), linha_rota.linha.horarios_de_saida))
    saidas.sort()
    return saidas

def cria_linhas_uniforme():
    return {
        '8012': LinhaRota(
            Linha(
                '8012',
                calcular_horarios_saidas([ 2, 1, 1, 1, 3, 5, 7, 7, 6, 6, 5, 4, 5, 7, 7, 6, 7, 6, 7, 6, 4, 5, 6, 5 ]),
                MediaPercurso([(0, 64), (6*60, 63), (10*60, 64), (15*60, 67), (21*60, 64)])
            ),
            Rota(
                ['1859', '1846', '1924', '1934', '2', '1930', '1920', '1839', '1922', '1863', '1857', '1926', '1871', '1938'],
                ['1918', '1914', '1922', '1887', '1806', '1813', '1791', '1811', '1841', '1804', '1867', '1796', '1800', '1892', '1809', '1832', '1830', "7"]
            )
        ),
        '8022': LinhaRota(
            Linha(
                '8022',
                calcular_horarios_saidas([ 3, 3, 2, 1, 3, 5, 9, 9, 7, 6, 5, 6, 8, 6, 6, 7, 7, 7, 7, 8, 6, 5, 6, 4 ]),
                MediaPercurso([(0, 67), (6*60, 67), (10*60, 67), (15*60, 68), (21*60, 67)])
            ),
            Rota (
                ['1861', '1865', '1924', '1899', '1934', '1904', '1', '1930', '1920', '3', '1818', '1826', '4', '1848', '1926', '5', '6', '1802', '1928', '1910'],
                ['1834', '1890', '1940', '1908', '1922', '1932', '1791', '1844', '1896', '8', '1936', '1928', '1912', '1920', '1832']
            )
        ),
        '8032': LinhaRota(
            Linha(
                '8032',
                calcular_horarios_saidas([ 2, 0, 0, 0, 0, 4, 5, 4, 5, 4, 3, 3, 4, 5, 3, 3, 4, 5, 5, 5, 3, 3, 4, 3 ]),
                MediaPercurso([(0, 32), (6*60, 35), (10*60, 32), (15*60, 33), (21*60, 32)])
            ),
            Rota (
                ['1859', '1813', '1846', '1841', '1839', '1863', '1857', '1796', '1867', '1800', "7", "1830", "1832"]
            )
        )
    }

def cria_linhas_sptrans():
    return {
        '8012': LinhaRota(
            Linha(
                '8012',
                [0*60 + 15, 0*60 + 35, 1*60 + 25, 2*60 + 8, 3*60 + 10, 4*60 + 00, 4*60 + 30, 4*60 + 55, 5*60 + 10, 5*60 + 20, 5*60 + 29, 5*60 + 39, 5*60 + 50, 6*60 + 00, 6*60 + 8, 6*60 + 17, 6*60 + 26, 6*60 + 34, 6*60 + 43, 6*60 + 52, 7*60 + 00, 7*60 + 9, 7*60 + 18, 7*60 + 27, 7*60 + 36, 7*60 + 45, 7*60 + 54, 8*60 + 4, 8*60 + 14, 8*60 + 24, 8*60 + 34, 8*60 + 44, 8*60 + 55, 9*60 + 6, 9*60 + 16, 9*60 + 26, 9*60 + 37, 9*60 + 48, 9*60 + 58, 10*60 + 8, 10*60 + 18, 10*60 + 28, 10*60 + 41, 10*60 + 54, 11*60 + 7, 11*60 + 20, 11*60 + 34, 11*60 + 49, 12*60 + 2, 12*60 + 15, 12*60 + 27, 12*60 + 39, 12*60 + 51, 13*60 + 3, 13*60 + 12, 13*60 + 20, 13*60 + 29, 13*60 + 38, 13*60 + 45, 13*60 + 54, 14*60 + 2, 14*60 + 11, 14*60 + 21, 14*60 + 30, 14*60 + 37, 14*60 + 44, 14*60 + 54, 15*60 + 5, 15*60 + 15, 15*60 + 25, 15*60 + 35, 15*60 + 44, 15*60 + 52, 16*60 + 00, 16*60 + 8, 16*60 + 17, 16*60 + 27, 16*60 + 37, 16*60 + 46, 16*60 + 54, 17*60 + 2, 17*60 + 10, 17*60 + 19, 17*60 + 29, 17*60 + 40, 17*60 + 51, 18*60 + 1, 18*60 + 11, 18*60 + 20, 18*60 + 29, 18*60 + 38, 18*60 + 47, 18*60 + 56, 19*60 + 5, 19*60 + 14, 19*60 + 23, 19*60 + 32, 19*60 + 41, 19*60 + 50, 20*60 + 5, 20*60 + 20, 20*60 + 35, 20*60 + 50, 21*60 + 4, 21*60 + 18, 21*60 + 31, 21*60 + 43, 21*60 + 55, 22*60 + 5, 22*60 + 15, 22*60 + 25, 22*60 + 35, 22*60 + 45, 22*60 + 55, 23*60 + 10, 23*60 + 25, 23*60 + 40, 23*60 + 47, 23*60 + 55],
                MediaPercurso([(0, 64), (7*60, 63), (10*60, 64), (17*60, 67), (20*60, 64)])
            ),
            Rota (
                ['1859', '1846', '1924', '1934', '2', '1930', '1920', '1839', '1922', '1863', '1857', '1926', '1871', '1938'],
                ['1918', '1914', '1922', '1887', '1806', '1813', '1791', '1811', '1841', '1804', '1867', '1796', '1800', '1892', '1809', '1832', '1830', "7"]
            )        
        ),
        '8022': LinhaRota(
            Linha(
                '8022',
                [0*60 + 15, 0*60 + 34, 0*60 + 52, 1*60 + 11, 1*60 + 36, 2*60 + 23, 3*60 + 15, 4*60 + 5, 4*60 + 30, 4*60 + 55, 5*60 + 10, 5*60 + 24, 5*60 + 33, 5*60 + 42, 5*60 + 51, 6*60 + 0, 6*60 + 6, 6*60 + 15, 6*60 + 24, 6*60 + 32, 6*60 + 39, 6*60 + 46, 6*60 + 52, 6*60 + 58, 7*60 + 5, 7*60 + 12, 7*60 + 18, 7*60 + 24, 7*60 + 32, 7*60 + 40, 7*60 + 47, 7*60 + 54, 7*60 + 59, 8*60 + 9, 8*60 + 19, 8*60 + 28, 8*60 + 37, 8*60 + 45, 8*60 + 53, 9*60 + 1, 9*60 + 9, 9*60 + 17, 9*60 + 26, 9*60 + 35, 9*60 + 44, 9*60 + 54, 10*60 + 4, 10*60 + 13, 10*60 + 23, 10*60 + 33, 10*60 + 42, 10*60 + 50, 11*60 + 0, 11*60 + 10, 11*60 + 20, 11*60 + 29, 11*60 + 39, 11*60 + 50, 12*60 + 0, 12*60 + 7, 12*60 + 14, 12*60 + 21, 12*60 + 29, 12*60 + 37, 12*60 + 46, 12*60 + 56, 13*60 + 7, 13*60 + 18, 13*60 + 31, 13*60 + 43, 13*60 + 54, 14*60 + 3, 14*60 + 10, 14*60 + 17, 14*60 + 25, 14*60 + 33, 14*60 + 42, 14*60 + 50, 14*60 + 57, 15*60 + 5, 15*60 + 12, 15*60 + 19, 15*60 + 27, 15*60 + 33, 15*60 + 41, 15*60 + 49, 15*60 + 57, 16*60 + 3, 16*60 + 10, 16*60 + 17, 16*60 + 24, 16*60 + 32, 16*60 + 41, 16*60 + 50, 16*60 + 58, 17*60 + 5, 17*60 + 12, 17*60 + 20, 17*60 + 28, 17*60 + 36, 17*60 + 44, 17*60 + 53, 18*60 + 3, 18*60 + 12, 18*60 + 21, 18*60 + 31, 18*60 + 42, 18*60 + 53, 19*60 + 2, 19*60 + 12, 19*60 + 22, 19*60 + 32, 19*60 + 41, 19*60 + 50, 19*60 + 58, 20*60 + 8, 20*60 + 18, 20*60 + 25, 20*60 + 33, 20*60 + 43, 20*60 + 54, 21*60 + 6, 21*60 + 17, 21*60 + 27, 21*60 + 38, 21*60 + 50, 22*60 + 1, 22*60 + 12, 22*60 + 22, 22*60 + 31, 22*60 + 41, 22*60 + 53, 23*60 + 9, 23*60 + 29, 23*60 + 43, 23*60 + 57],
                MediaPercurso([(0, 67), (7*60, 67), (10*60, 67), (17*60, 68), (20*60, 67)])
            ),
            Rota (
                ['1861', '1865', '1924', '1899', '1934', '1904', '1', '1930', '1920', '3', '1818', '1826', '4', '1848', '1926', '5', '6', '1802', '1928', '1910'],
                ['1834', '1890', '1940', '1908', '1922', '1932', '1791', '1844', '1896', '8', '1936', '1928', '1912', '1920', '1832']
            )        
        ),
        '8032': LinhaRota(
            Linha(
                '8032',
                [0*60 + 15, 0*60 + 40, 5*60 + 0, 5*60 + 30, 6*60 + 5, 6*60 + 17, 6*60 + 29, 6*60 + 41, 6*60 + 53, 7*60 + 5, 7*60 + 17, 7*60 + 29, 7*60 + 41, 7*60 + 53, 8*60 + 8, 8*60 + 23, 8*60 + 38, 8*60 + 53, 9*60 + 8, 9*60 + 23, 9*60 + 38, 9*60 + 53, 10*60 + 8, 10*60 + 23, 10*60 + 38, 10*60 + 53, 11*60 + 8, 11*60 + 23, 11*60 + 38, 11*60 + 53, 12*60 + 3, 12*60 + 13, 12*60 + 23, 12*60 + 33, 12*60 + 43, 12*60 + 53, 13*60 + 5, 13*60 + 16, 13*60 + 27, 13*60 + 38, 13*60 + 49, 14*60 + 3, 14*60 + 17, 14*60 + 34, 14*60 + 53, 15*60 + 8, 15*60 + 23, 15*60 + 40, 15*60 + 55, 16*60 + 6, 16*60 + 17, 16*60 + 29, 16*60 + 41, 16*60 + 53, 17*60 + 4, 17*60 + 16, 17*60 + 28, 17*60 + 39, 17*60 + 51, 18*60 + 3, 18*60 + 14, 18*60 + 25, 18*60 + 36, 18*60 + 47, 18*60 + 57, 19*60 + 7, 19*60 + 18, 19*60 + 29, 19*60 + 40, 19*60 + 50, 20*60 + 5, 20*60 + 20, 20*60 + 35, 20*60 + 50, 21*60 + 6, 21*60 + 22, 21*60 + 38, 21*60 + 54, 22*60 + 4, 22*60 + 14, 22*60 + 24, 22*60 + 34, 22*60 + 44, 22*60 + 54, 23*60 + 6, 23*60 + 41],
                MediaPercurso([(0, 32), (7*60, 35), (10*60, 32), (17*60, 33), (20*60, 32)])
            ),
            Rota (
                ['1859', '1813', '1846', '1841', '1839', '1863', '1857', '1796', '1867', '1800', "7", "1830", "1832"]
            )       
        )
    }

def junta_demanda(demanda1, demanda2):
    demanda_total = {}
    for dia in demanda1.keys():
        demanda_total[dia] = {}
        for horario in demanda1[dia].keys():
            demanda_total[dia][horario] = {}
            for ponto in demanda1[dia][horario]:
                demanda_total[dia][horario][ponto] = {}
                if ponto in demanda2[dia][horario]:
                    for linha in demanda1[dia][horario][ponto]:
                        demanda_total[dia][horario][ponto][linha] = demanda1[dia][horario][ponto][linha] + demanda2[dia][horario][ponto].get(linha, 0)
                else:
                    for linha in demanda1[dia][horario][ponto]:
                        demanda_total[dia][horario][ponto][linha] = demanda1[dia][horario][ponto][linha]
            for ponto in demanda2[dia][horario]:
                demanda_total[dia][horario][ponto] = demanda_total[dia][horario].get(ponto, {})
                if ponto in demanda1[dia][horario]:
                    for linha in demanda2[dia][horario][ponto]:
                        demanda_total[dia][horario][ponto][linha] = demanda2[dia][horario][ponto][linha] + demanda1[dia][horario][ponto].get(linha, 0)
                else:
                    for linha in demanda2[dia][horario][ponto]:
                        demanda_total[dia][horario][ponto][linha] = demanda2[dia][horario][ponto][linha]
        
    return demanda_total

def soma_demanda(demanda):
    soma = {}
    for dia in demanda.keys():
        soma[dia] = {}
        for horario in demanda[dia].keys():
            soma[dia][horario] = 0
            for ponto in demanda[dia][horario].keys():
                for linha in demanda[dia][horario][ponto].keys():
                    soma[dia][horario] += demanda[dia][horario][ponto][linha]
    return soma

def porcentagem_chegada_total(soma_total, soma_restante):
    porcentagem = {}
    for dia in soma_total.keys():
        porcentagem[dia] = {}
        for horario in soma_total[dia].keys():
            porcentagem[dia][horario] = 1 - soma_restante[dia][horario]/soma_total[dia][horario]
    return porcentagem

def calcula_atendimento_ida(linhas, demanda_butanta, demanda_p3, saidas):
    horarios = [480, 1140]
    dias = ["seg", "ter", "qua", "qui", "sex"]
    for saida in saidas:
        for dia in dias:
            for horario in horarios:
                if horario-120 < saida.horario < horario:
                    distribui_pessoas(linhas, demanda_butanta[dia][horario], saida.linha, 100, 'ida')
                    if saida.linha != '8032':
                        distribui_pessoas(linhas, demanda_p3[dia][horario], saida.linha, 50, 'volta')

def calcula_atendimento_volta(linhas, demanda_butanta, demanda_p3, saidas):
    horarios = [1110]
    dias = ["seg", "ter", "qua", "qui", "sex"]
    for saida in saidas:
        for dia in dias:
            for horario in horarios:
                if horario-60 < saida.horario < horario+30:
                    if saida.linha != '8032':
                        distribui_pessoas(linhas, demanda_p3[dia][horario], saida.linha, 50, 'ida')
                        distribui_pessoas(linhas, demanda_butanta[dia][horario], saida.linha, 100, 'volta')
                    else:
                        distribui_pessoas(linhas, demanda_butanta[dia][horario], saida.linha, 100, 'ida')

def distribui_pessoas(linhas, demanda, id_linha, pessoas, caminho):
    linha = linhas[id_linha]
    if caminho == 'ida':
        rota = linha.rota.ida
    else:
        rota = linha.rota.volta
    for ponto in rota:
        if (id_to_nome[ponto] not in demanda or id_linha not in demanda[id_to_nome[ponto]]):
            continue
        frequencia = porc_de_linha_desce_em_ponto(id_to_nome[ponto], id_linha, demanda)
        demanda[id_to_nome[ponto]][id_linha] -= pessoas * frequencia
        if demanda[id_to_nome[ponto]][id_linha] < 0:
            demanda[id_to_nome[ponto]][id_linha] = 0

def porc_de_linha_desce_em_ponto(ponto_alvo, linha, demanda):
    sum_pessoas = 0
    for ponto in demanda:
        if linha not in demanda[ponto]:
            continue
        sum_pessoas += demanda[ponto][linha]
    if linha not in demanda[ponto_alvo]:
        return 0
    if sum_pessoas == 0:
        return 0
    return demanda[ponto_alvo][linha] / sum_pessoas

def trata_demanda_percentual(demanda, porc):
    for dia in demanda:
        for horario in demanda[dia]:
            for ponto in demanda[dia][horario]:
                for linha in demanda[dia][horario][ponto]:
                    demanda[dia][horario][ponto][linha] = round(demanda[dia][horario][ponto][linha] * porc)

def porcentagem_chegada_por_ponto(demanda_total, demanda_restante):
    atendimento = {}
    for dia in demanda_total:
        atendimento[dia] = {}
        for horario in demanda_total[dia]:
            atendimento[dia][horario] = {}
            for ponto in demanda_total[dia][horario]:
                atendimento[dia][horario][ponto] = {}
                for linha in demanda_total[dia][horario][ponto]:
                    atendimento[dia][horario][ponto][linha] = 1 - (demanda_restante[dia][horario][ponto][linha] / demanda_total[dia][horario][ponto][linha])       
    return atendimento

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

# Simulacao
def main():
    if len(sys.argv) < 2:
        print('Passe todos os parâmetros!')
        exit(1)

    SIMULACAO = sys.argv[1].lower()

    print("SIMULANDO MODELO " + SIMULACAO)

    if SIMULACAO == "uniforme":
        linhas_rotas = cria_linhas_uniforme()
    elif SIMULACAO == "sptrans":
        linhas_rotas = cria_linhas_sptrans()
    else:
        exit(1)

    trata_demanda_percentual(demanda_ida_butanta, 0.8)
    trata_demanda_percentual(demanda_ida_butanta_func, 0.8)
    trata_demanda_percentual(demanda_volta_butanta, 0.8)
    trata_demanda_percentual(demanda_ida_p3, 0.2)
    trata_demanda_percentual(demanda_ida_p3_func, 0.2)
    trata_demanda_percentual(demanda_volta_p3, 0.2)

    remove_demanda_inexistente(demanda_ida_butanta)
    remove_demanda_inexistente(demanda_ida_butanta_func)
    remove_demanda_inexistente(demanda_volta_butanta)
    remove_demanda_inexistente(demanda_ida_p3)
    remove_demanda_inexistente(demanda_ida_p3_func)
    remove_demanda_inexistente(demanda_volta_p3)

    demanda_ida_alunos = junta_demanda(demanda_ida_butanta, demanda_ida_p3)
    demanda_ida_func = junta_demanda(demanda_ida_butanta_func, demanda_ida_p3_func)
    demanda_ida_completa = junta_demanda(demanda_ida_alunos, demanda_ida_func)
    demanda_volta_alunos = junta_demanda(demanda_volta_butanta, demanda_volta_p3)

    demanda_ida_completa_butanta = junta_demanda(demanda_ida_butanta, demanda_ida_butanta_func)
    demanda_ida_completa_p3 = junta_demanda(demanda_ida_p3, demanda_ida_p3_func)

    saidas = cria_eventos_saidas(linhas_rotas)

    total = soma_demanda(demanda_ida_completa)
    pprint(total)
    state = calcula_atendimento_ida(linhas_rotas, demanda_ida_completa_butanta, demanda_ida_completa_p3, saidas)
    demanda_ida_restante = junta_demanda(demanda_ida_completa_butanta, demanda_ida_completa_p3)
    restante = soma_demanda(demanda_ida_restante)
    pprint(porcentagem_chegada_total(total, restante))
    pprint(porcentagem_chegada_por_ponto(demanda_ida_completa, demanda_ida_restante))

    total_volta = soma_demanda(demanda_volta_alunos)
    pprint(total_volta)
    state = calcula_atendimento_volta(linhas_rotas, demanda_volta_butanta, demanda_volta_p3, saidas)
    demanda_volta_restante = junta_demanda(demanda_volta_butanta, demanda_volta_p3)
    restante = soma_demanda(demanda_volta_restante)
    pprint(porcentagem_chegada_total(total_volta, restante))

if __name__ == "__main__":
    main()
