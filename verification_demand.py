from bisect import insort, bisect_left
from pprint import pprint
#import matplotlib.pyplot as plt
import sys
from verification import calcular_horarios_saidas
from verification import verifica_chegadas
from verification import handle_saida
from verification import Evento, Linha, MediaPercurso
from pontos_ajustados import demanda_completa
from pontos_ajustados_volta import demanda_completa_volta
from copy import deepcopy

class LinhaRota():
    def __init__(self, linha, rota):
        self.linha = linha
        self.rota = rota

class Rota():
    def __init__(self, frequencia_por_horario):
        self.frequencia_por_horario = frequencia_por_horario

    def em(self, horario):
        horarios_iniciais = list(map(lambda x: x[0], self.frequencia_por_horario))
        index = bisect_left(horarios_iniciais, horario)
        if index == len(horarios_iniciais) or horarios_iniciais[index] != horario:
            index = index-1
        return self.frequencia_por_horario[index][1]

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
    "1887": "Ponto Clube dos funcionários",
    "1890": "Física",
    "1892": "IAG",
    "1896": "Butantan",
    "1899": "Biblioteca Farmácia e Química",
    "1904": "História e Geografia",
    "1908": "CEPAM",
    "1910": "Rua do Lago",
    "1912": "Geociências I",
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
    "1940": "Cocesp II"
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
                [(0, {"1791": (1/28), "1920": 0, "1826": 0, "1818": 0, "1890": 0, "1796": (1/28), "1800": (1/28), "1804": (1/28), "1806": (1/28), "1809": (1/28), "1811": (1/28), "1813": (1/28), "1830": (1/28), "1832": (1/28), "1839": (1/28), "1841": (1/28), "1846": (1/28), "1857": (1/28), "1859": (1/28), "1863": (1/28), "1867": (1/28), "1871": (1/28), "1887": (1/28), "1892": (1/28), "1912": (1/28), "1918": (1/28), "1922": (1/28), "1924": (1/28), "1926": (1/28), "1930": (1/28), "1934": (1/28), "1938": (1/28)})]
            )
        ),
        '8022': LinhaRota(
            Linha(
                '8022',
                calcular_horarios_saidas([ 3, 3, 2, 1, 3, 5, 9, 9, 7, 6, 5, 6, 8, 6, 6, 7, 7, 7, 7, 8, 6, 5, 6, 4 ]),
                MediaPercurso([(0, 67), (6*60, 67), (10*60, 67), (15*60, 68), (21*60, 67)])
            ),
            Rota (
                [(0, {"1791": (1/28), "1887": 0, "1796": 0, "1863": 0, "1867": 0, "1926": 0, "1841": 0, "1934": 0, "1930": 0, "1802": (1/28), "1818": (1/28), "1826": (1/28), "1830": (1/28), "1832": (1/28), "1834": (1/28), "1844": (1/28), "1848": (1/28), "1850": (1/28), "1861": (1/28), "1865": (1/28), "1890": (1/28), "1896": (1/28), "1899": (1/28), "1904": (1/28), "1908": (1/28), "1910": (1/28), "1912": (1/28), "1918": (1/28), "1920": (1/28), "1922": (1/28), "1924": (1/28), "1928": (1/28), "1932": (1/28), "1936": (1/28), "1940": (1/28)})]
            )
        ),
        '8032': LinhaRota(
            Linha(
                '8032',
                calcular_horarios_saidas([ 2, 0, 0, 0, 0, 4, 5, 4, 5, 4, 3, 3, 4, 5, 3, 3, 4, 5, 5, 5, 3, 3, 4, 3 ]),
                MediaPercurso([(0, 32), (6*60, 35), (10*60, 32), (15*60, 33), (21*60, 32)])
            ),
            Rota (
                [(0, {"1791": (1/15), "1841": 0, "1796": (1/15), "1800": (1/15), "1813": (1/15), "1818": (1/15), "1830": (1/15), "1832": (1/15), "1834": (1/15), "1839": (1/15), "1846": (1/15), "1859": (1/15), "1857": (1/15), "1867": (1/15), "1863": (1/15)})]
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
                [(0, {"1791": (1/28), "1920": 0, "1826": 0, "1818": 0, "1890": 0, "1796": (1/28), "1800": (1/28), "1804": (1/28), "1806": (1/28), "1809": (1/28), "1811": (1/28), "1813": (1/28), "1830": (1/28), "1832": (1/28), "1839": (1/28), "1841": (1/28), "1846": (1/28), "1857": (1/28), "1859": (1/28), "1863": (1/28), "1867": (1/28), "1871": (1/28), "1887": (1/28), "1892": (1/28), "1912": (1/28), "1918": (1/28), "1922": (1/28), "1924": (1/28), "1926": (1/28), "1930": (1/28), "1934": (1/28), "1938": (1/28)})]
            )        
        ),
        '8022': LinhaRota(
            Linha(
                '8022',
                [0*60 + 15, 0*60 + 34, 0*60 + 52, 1*60 + 11, 1*60 + 36, 2*60 + 23, 3*60 + 15, 4*60 + 5, 4*60 + 30, 4*60 + 55, 5*60 + 10, 5*60 + 24, 5*60 + 33, 5*60 + 42, 5*60 + 51, 6*60 + 0, 6*60 + 6, 6*60 + 15, 6*60 + 24, 6*60 + 32, 6*60 + 39, 6*60 + 46, 6*60 + 52, 6*60 + 58, 7*60 + 5, 7*60 + 12, 7*60 + 18, 7*60 + 24, 7*60 + 32, 7*60 + 40, 7*60 + 47, 7*60 + 54, 7*60 + 59, 8*60 + 9, 8*60 + 19, 8*60 + 28, 8*60 + 37, 8*60 + 45, 8*60 + 53, 9*60 + 1, 9*60 + 9, 9*60 + 17, 9*60 + 26, 9*60 + 35, 9*60 + 44, 9*60 + 54, 10*60 + 4, 10*60 + 13, 10*60 + 23, 10*60 + 33, 10*60 + 42, 10*60 + 50, 11*60 + 0, 11*60 + 10, 11*60 + 20, 11*60 + 29, 11*60 + 39, 11*60 + 50, 12*60 + 0, 12*60 + 7, 12*60 + 14, 12*60 + 21, 12*60 + 29, 12*60 + 37, 12*60 + 46, 12*60 + 56, 13*60 + 7, 13*60 + 18, 13*60 + 31, 13*60 + 43, 13*60 + 54, 14*60 + 3, 14*60 + 10, 14*60 + 17, 14*60 + 25, 14*60 + 33, 14*60 + 42, 14*60 + 50, 14*60 + 57, 15*60 + 5, 15*60 + 12, 15*60 + 19, 15*60 + 27, 15*60 + 33, 15*60 + 41, 15*60 + 49, 15*60 + 57, 16*60 + 3, 16*60 + 10, 16*60 + 17, 16*60 + 24, 16*60 + 32, 16*60 + 41, 16*60 + 50, 16*60 + 58, 17*60 + 5, 17*60 + 12, 17*60 + 20, 17*60 + 28, 17*60 + 36, 17*60 + 44, 17*60 + 53, 18*60 + 3, 18*60 + 12, 18*60 + 21, 18*60 + 31, 18*60 + 42, 18*60 + 53, 19*60 + 2, 19*60 + 12, 19*60 + 22, 19*60 + 32, 19*60 + 41, 19*60 + 50, 19*60 + 58, 20*60 + 8, 20*60 + 18, 20*60 + 25, 20*60 + 33, 20*60 + 43, 20*60 + 54, 21*60 + 6, 21*60 + 17, 21*60 + 27, 21*60 + 38, 21*60 + 50, 22*60 + 1, 22*60 + 12, 22*60 + 22, 22*60 + 31, 22*60 + 41, 22*60 + 53, 23*60 + 9, 23*60 + 29, 23*60 + 43, 23*60 + 57],
                MediaPercurso([(0, 67), (7*60, 67), (10*60, 67), (17*60, 68), (20*60, 67)])
            ),
            Rota (
                [(0, {"1791": (1/28), "1887": 0, "1796": 0, "1863": 0, "1867": 0, "1934":0, "1926": 0, "1841": 0, "1930": 0, "1802": (1/28), "1818": (1/28), "1826": (1/28), "1830": (1/28), "1832": (1/28), "1834": (1/28), "1844": (1/28), "1848": (1/28), "1850": (1/28), "1861": (1/28), "1865": (1/28), "1890": (1/28), "1896": (1/28), "1899": (1/28), "1904": (1/28), "1908": (1/28), "1910": (1/28), "1912": (1/28), "1918": (1/28), "1920": (1/28), "1922": (1/28), "1924": (1/28), "1928": (1/28), "1932": (1/28), "1936": (1/28), "1940": (1/28)})]
            )        
        ),
        '8032': LinhaRota(
            Linha(
                '8032',
                [0*60 + 15, 0*60 + 40, 5*60 + 0, 5*60 + 30, 6*60 + 5, 6*60 + 17, 6*60 + 29, 6*60 + 41, 6*60 + 53, 7*60 + 5, 7*60 + 17, 7*60 + 29, 7*60 + 41, 7*60 + 53, 8*60 + 8, 8*60 + 23, 8*60 + 38, 8*60 + 53, 9*60 + 8, 9*60 + 23, 9*60 + 38, 9*60 + 53, 10*60 + 8, 10*60 + 23, 10*60 + 38, 10*60 + 53, 11*60 + 8, 11*60 + 23, 11*60 + 38, 11*60 + 53, 12*60 + 3, 12*60 + 13, 12*60 + 23, 12*60 + 33, 12*60 + 43, 12*60 + 53, 13*60 + 5, 13*60 + 16, 13*60 + 27, 13*60 + 38, 13*60 + 49, 14*60 + 3, 14*60 + 17, 14*60 + 34, 14*60 + 53, 15*60 + 8, 15*60 + 23, 15*60 + 40, 15*60 + 55, 16*60 + 6, 16*60 + 17, 16*60 + 29, 16*60 + 41, 16*60 + 53, 17*60 + 4, 17*60 + 16, 17*60 + 28, 17*60 + 39, 17*60 + 51, 18*60 + 3, 18*60 + 14, 18*60 + 25, 18*60 + 36, 18*60 + 47, 18*60 + 57, 19*60 + 7, 19*60 + 18, 19*60 + 29, 19*60 + 40, 19*60 + 50, 20*60 + 5, 20*60 + 20, 20*60 + 35, 20*60 + 50, 21*60 + 6, 21*60 + 22, 21*60 + 38, 21*60 + 54, 22*60 + 4, 22*60 + 14, 22*60 + 24, 22*60 + 34, 22*60 + 44, 22*60 + 54, 23*60 + 6, 23*60 + 41],
                MediaPercurso([(0, 32), (7*60, 35), (10*60, 32), (17*60, 33), (20*60, 32)])
            ),
            Rota (
                [(0, {"1791": (1/15), "1841": 0, "1796": (1/15), "1800": (1/15), "1813": (1/15), "1818": (1/15), "1830": (1/15), "1832": (1/15), "1834": (1/15), "1839": (1/15), "1846": (1/15), "1859": (1/15), "1857": (1/15), "1867": (1/15), "1863": (1/15)})]
            )       
        )
    }

def cria_demanda(linhas):
    pontos_onibus = ["1791", "1796", "1800", "1794", "1802", "1804", "1806", "1809", "1811", "1813", "1818", "1826", "1830", "1832", "1834", "1839", "1841", "1844", "1846", "1848", "1850", "1857", "1859", "1861", "1863", "1865", "1867", "1871", "1887", "1890", "1892", "1896", "1899", "1904", "1908", "1910", "1912", "1916", "1918", "1920", "1922", "1924", "1926", "1928", "1930", "1932", "1934", "1936", "1938", "1940"]
    demanda = {"seg": {480: {}}}
    for ponto in pontos_onibus:
        demanda["seg"][480][ponto] = {}
        for linha in linhas.keys():
            if ponto in linhas[linha].rota.frequencia_por_horario[0][1]:
                demanda["seg"][480][ponto][linha] = 100
    return demanda

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

def porcentagem_chegada(soma_total, soma_restante):
    porcentagem = {}
    for dia in soma_total.keys():
        porcentagem[dia] = {}
        for horario in soma_total[dia].keys():
            porcentagem[dia][horario] = 1 - soma_restante[dia][horario]/soma_total[dia][horario]
    return porcentagem


def calcula_atendimento_ida(linhas, demanda, saidas):
    horarios = [480, 1080]
    dias = ["seg", "ter", "qua", "qui", "sex"]
    for saida in saidas:
        for dia in dias:
            for horario in horarios:
                if horario-120 < saida.horario < horario:
                    distribui_pessoas(dia, horario, linhas, demanda[dia][horario], saida)

def distribui_pessoas(dia, hora, linhas, demanda, saida):
    pessoas = 100
    linha = linhas[saida.linha]
    freq = linha.rota.em(saida.horario)
    for ponto in freq.keys():

        if (id_to_nome[ponto] not in demanda or saida.linha not in demanda[id_to_nome[ponto]]):
            continue
        frequencia = porc_de_linha_desce_em_ponto(id_to_nome[ponto], saida.linha, demanda)
        demanda[id_to_nome[ponto]][saida.linha] -= pessoas * frequencia
        if demanda[id_to_nome[ponto]][saida.linha] < 0:
            demanda[id_to_nome[ponto]][saida.linha] = 0

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

def calcula_atendimento_volta(linhas, demanda, saidas):
    horarios = [1110]
    dias = ["seg", "ter", "qua", "qui", "sex"]
    for saida in saidas:
        for dia in dias:
            for horario in horarios:
                if horario-60 < saida.horario < horario+30:
                    distribui_pessoas(dia, horario, linhas, demanda[dia][horario], saida)

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

    demanda = deepcopy(demanda_completa)
    demanda_volta = deepcopy(demanda_completa_volta)

    saidas = cria_eventos_saidas(linhas_rotas)

    total = soma_demanda(demanda)
    pprint(total)
    state = calcula_atendimento_ida(linhas_rotas, demanda, saidas)
    restante = soma_demanda(demanda)
    pprint(porcentagem_chegada(total, restante))

    total_volta = soma_demanda(demanda_volta)
    pprint(total_volta)
    state = calcula_atendimento_volta(linhas_rotas, demanda_volta, saidas)
    restante = soma_demanda(demanda_volta)
    pprint(porcentagem_chegada(total_volta, restante))

if __name__ == "__main__":
    main()
