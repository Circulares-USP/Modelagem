from bisect import insort, bisect_left
import matplotlib.pyplot as plt
import sys

# Approaches:
# 1. Testar uniformemente
# 2. Testar "de qualquer forma" (podendo sair de qualquer forma)

# Dados:
# - O número de saídas por horário
# - Média do Percurso (dependendo do horário)

# Definicoes:
# - Estamos usando o approach 1
# - 

# TODO: Verificar dados
# - Descobrir se tem tempo de parada mínimo
# - Verificar dados das saídas com Hermes
# - Verificar a média de tempo com os dados da API

# Utils

def calcular_horarios_saidas(saidas_por_hora):
    ret = []
    for hour, num_saidas in enumerate(saidas_por_hora):
        if num_saidas > 0:
            saidas_a_cada = 60 / num_saidas
            minuto = 0
            while round(minuto) < 60:
                ret.append(60*hour + round(minuto))
                minuto += saidas_a_cada
    return ret

def cria_linhas_uniforme():
    return {
        '8012': Linha(
            '8012',
            calcular_horarios_saidas([ 2, 1, 1, 1, 3, 5, 7, 7, 6, 6, 5, 4, 5, 7, 7, 6, 7, 6, 7, 6, 4, 5, 6, 5 ]),
            MediaPercurso([(0, 64), (6*60, 63), (10*60, 64), (15*60, 67), (21*60, 64)]),
        ),
        '8022': Linha(
            '8022',
            calcular_horarios_saidas([ 3, 3, 2, 1, 3, 5, 9, 9, 7, 6, 5, 6, 8, 6, 6, 7, 7, 7, 7, 8, 6, 5, 6, 4 ]),
            MediaPercurso([(0, 67), (6*60, 67), (10*60, 67), (15*60, 68), (21*60, 67)]),
        ),
        '8032': Linha(
            '8032',
            calcular_horarios_saidas([ 2, 0, 0, 0, 0, 4, 5, 4, 5, 4, 3, 3, 4, 5, 3, 3, 4, 5, 5, 5, 3, 3, 4, 3 ]),
            MediaPercurso([(0, 32), (6*60, 35), (10*60, 32), (15*60, 33), (21*60, 32)]),
        )
    }

def cria_linhas_sptrans():
    return {
        '8012': Linha(
            '8012',
            [0*60 + 15, 0*60 + 35, 1*60 + 25, 2*60 + 8, 3*60 + 10, 4*60 + 00, 4*60 + 30, 4*60 + 55, 5*60 + 10, 5*60 + 20, 5*60 + 29, 5*60 + 39, 5*60 + 50, 6*60 + 00, 6*60 + 8, 6*60 + 17, 6*60 + 26, 6*60 + 34, 6*60 + 43, 6*60 + 52, 7*60 + 00, 7*60 + 9, 7*60 + 18, 7*60 + 27, 7*60 + 36, 7*60 + 45, 7*60 + 54, 8*60 + 4, 8*60 + 14, 8*60 + 24, 8*60 + 34, 8*60 + 44, 8*60 + 55, 9*60 + 6, 9*60 + 16, 9*60 + 26, 9*60 + 37, 9*60 + 48, 9*60 + 58, 10*60 + 8, 10*60 + 18, 10*60 + 28, 10*60 + 41, 10*60 + 54, 11*60 + 7, 11*60 + 20, 11*60 + 34, 11*60 + 49, 12*60 + 2, 12*60 + 15, 12*60 + 27, 12*60 + 39, 12*60 + 51, 13*60 + 3, 13*60 + 12, 13*60 + 20, 13*60 + 29, 13*60 + 38, 13*60 + 45, 13*60 + 54, 14*60 + 2, 14*60 + 11, 14*60 + 21, 14*60 + 30, 14*60 + 37, 14*60 + 44, 14*60 + 54, 15*60 + 5, 15*60 + 15, 15*60 + 25, 15*60 + 35, 15*60 + 44, 15*60 + 52, 16*60 + 00, 16*60 + 8, 16*60 + 17, 16*60 + 27, 16*60 + 37, 16*60 + 46, 16*60 + 54, 17*60 + 2, 17*60 + 10, 17*60 + 19, 17*60 + 29, 17*60 + 40, 17*60 + 51, 18*60 + 1, 18*60 + 11, 18*60 + 20, 18*60 + 29, 18*60 + 38, 18*60 + 47, 18*60 + 56, 19*60 + 5, 19*60 + 14, 19*60 + 23, 19*60 + 32, 19*60 + 41, 19*60 + 50, 20*60 + 5, 20*60 + 20, 20*60 + 35, 20*60 + 50, 21*60 + 4, 21*60 + 18, 21*60 + 31, 21*60 + 43, 21*60 + 55, 22*60 + 5, 22*60 + 15, 22*60 + 25, 22*60 + 35, 22*60 + 45, 22*60 + 55, 23*60 + 10, 23*60 + 25, 23*60 + 40, 23*60 + 47, 23*60 + 55],
            MediaPercurso([(0, 64), (7*60, 63), (10*60, 64), (17*60, 67), (20*60, 64)]),
        ),
        '8022': Linha(
            '8022',
            [0*60 + 15, 0*60 + 34, 0*60 + 52, 1*60 + 11, 1*60 + 36, 2*60 + 23, 3*60 + 15, 4*60 + 5, 4*60 + 30, 4*60 + 55, 5*60 + 10, 5*60 + 24, 5*60 + 33, 5*60 + 42, 5*60 + 51, 6*60 + 0, 6*60 + 6, 6*60 + 15, 6*60 + 24, 6*60 + 32, 6*60 + 39, 6*60 + 46, 6*60 + 52, 6*60 + 58, 7*60 + 5, 7*60 + 12, 7*60 + 18, 7*60 + 24, 7*60 + 32, 7*60 + 40, 7*60 + 47, 7*60 + 54, 7*60 + 59, 8*60 + 9, 8*60 + 19, 8*60 + 28, 8*60 + 37, 8*60 + 45, 8*60 + 53, 9*60 + 1, 9*60 + 9, 9*60 + 17, 9*60 + 26, 9*60 + 35, 9*60 + 44, 9*60 + 54, 10*60 + 4, 10*60 + 13, 10*60 + 23, 10*60 + 33, 10*60 + 42, 10*60 + 50, 11*60 + 0, 11*60 + 10, 11*60 + 20, 11*60 + 29, 11*60 + 39, 11*60 + 50, 12*60 + 0, 12*60 + 7, 12*60 + 14, 12*60 + 21, 12*60 + 29, 12*60 + 37, 12*60 + 46, 12*60 + 56, 13*60 + 7, 13*60 + 18, 13*60 + 31, 13*60 + 43, 13*60 + 54, 14*60 + 3, 14*60 + 10, 14*60 + 17, 14*60 + 25, 14*60 + 33, 14*60 + 42, 14*60 + 50, 14*60 + 57, 15*60 + 5, 15*60 + 12, 15*60 + 19, 15*60 + 27, 15*60 + 33, 15*60 + 41, 15*60 + 49, 15*60 + 57, 16*60 + 3, 16*60 + 10, 16*60 + 17, 16*60 + 24, 16*60 + 32, 16*60 + 41, 16*60 + 50, 16*60 + 58, 17*60 + 5, 17*60 + 12, 17*60 + 20, 17*60 + 28, 17*60 + 36, 17*60 + 44, 17*60 + 53, 18*60 + 3, 18*60 + 12, 18*60 + 21, 18*60 + 31, 18*60 + 42, 18*60 + 53, 19*60 + 2, 19*60 + 12, 19*60 + 22, 19*60 + 32, 19*60 + 41, 19*60 + 50, 19*60 + 58, 20*60 + 8, 20*60 + 18, 20*60 + 25, 20*60 + 33, 20*60 + 43, 20*60 + 54, 21*60 + 6, 21*60 + 17, 21*60 + 27, 21*60 + 38, 21*60 + 50, 22*60 + 1, 22*60 + 12, 22*60 + 22, 22*60 + 31, 22*60 + 41, 22*60 + 53, 23*60 + 9, 23*60 + 29, 23*60 + 43, 23*60 + 57],
            MediaPercurso([(0, 67), (7*60, 67), (10*60, 67), (17*60, 68), (20*60, 67)]),
        ),
        '8032': Linha(
            '8032',
            [0*60 + 15, 0*60 + 40, 5*60 + 0, 5*60 + 30, 6*60 + 5, 6*60 + 17, 6*60 + 29, 6*60 + 41, 6*60 + 53, 7*60 + 5, 7*60 + 17, 7*60 + 29, 7*60 + 41, 7*60 + 53, 8*60 + 8, 8*60 + 23, 8*60 + 38, 8*60 + 53, 9*60 + 8, 9*60 + 23, 9*60 + 38, 9*60 + 53, 10*60 + 8, 10*60 + 23, 10*60 + 38, 10*60 + 53, 11*60 + 8, 11*60 + 23, 11*60 + 38, 11*60 + 53, 12*60 + 3, 12*60 + 13, 12*60 + 23, 12*60 + 33, 12*60 + 43, 12*60 + 53, 13*60 + 5, 13*60 + 16, 13*60 + 27, 13*60 + 38, 13*60 + 49, 14*60 + 3, 14*60 + 17, 14*60 + 34, 14*60 + 53, 15*60 + 8, 15*60 + 23, 15*60 + 40, 15*60 + 55, 16*60 + 6, 16*60 + 17, 16*60 + 29, 16*60 + 41, 16*60 + 53, 17*60 + 4, 17*60 + 16, 17*60 + 28, 17*60 + 39, 17*60 + 51, 18*60 + 3, 18*60 + 14, 18*60 + 25, 18*60 + 36, 18*60 + 47, 18*60 + 57, 19*60 + 7, 19*60 + 18, 19*60 + 29, 19*60 + 40, 19*60 + 50, 20*60 + 5, 20*60 + 20, 20*60 + 35, 20*60 + 50, 21*60 + 6, 21*60 + 22, 21*60 + 38, 21*60 + 54, 22*60 + 4, 22*60 + 14, 22*60 + 24, 22*60 + 34, 22*60 + 44, 22*60 + 54, 23*60 + 6, 23*60 + 41],
            MediaPercurso([(0, 32), (7*60, 35), (10*60, 32), (17*60, 33), (20*60, 32)]),
        )
    }

def cria_eventos_saidas(linhas):
    saidas = []
    for id, linha in linhas.items():
        saidas += list(map(lambda n: Evento(id, n), linha.horarios_de_saida))
    saidas.sort()
    return saidas

def formata_hora(minutos):
    return f'{(minutos // 60):02}:{(minutos % 60):02}'

def modifica_onibus_ativos(num_ativos, evento, op):
    ultimo_ativo = num_ativos[-1]
    horario = evento.horario
    ativo_atual = num_ativos[-1][1][:]
    index_linha = int(evento.linha[2]) - 1
    ativo_atual[index_linha] += op

    if ultimo_ativo[0] == evento.horario:
        num_ativos.pop(-1)

    num_ativos.append((horario, ativo_atual, sum(ativo_atual)))

def verifica_chegadas(horario_saida, state):

    novos_onibus = 0

    ind_chegadas = 0
    while ind_chegadas < len(state.chegadas):
        hora_chegada = state.chegadas[ind_chegadas].horario
        if hora_chegada < horario_saida:
            modifica_onibus_ativos(state.onibus_ativos, state.chegadas[ind_chegadas], -1)
            novos_onibus += 1
        else:
            break
        ind_chegadas += 1
    
    state.chegadas = state.chegadas[novos_onibus:]
    state.onibus_disponiveis += novos_onibus

    return novos_onibus

def atrasa_saida(saida, novo_horario, state):
    saida.horario = novo_horario
    modifica_onibus_ativos(state.onibus_ativos, state.chegadas[0], -1)
    state.chegadas = state.chegadas[1:]
    state.onibus_disponiveis += 1

def handle_saida(linhas, saida, state):
    media_percurso = linhas[saida.linha].media.em(saida.horario)
    evento_chegada = Evento(saida.linha, saida.horario + media_percurso)
    insort(state.chegadas, evento_chegada)
    modifica_onibus_ativos(state.onibus_ativos, saida, +1)
    state.onibus_disponiveis -= 1

# Algoritmo:
# 1. Calcular os horários de saída
# 2. for incrementando os minutos
#    - Adiciona os onibus que chegaram
#    - Conto os onibus que precisam sair agora
#    - Se tem onibus disponivel,
#      - Decrementar os onibus disponiveis e tirar da lista dos horarios de saida e adiciona na lista de horários de chegada
#    - Se minutos % 60, verifico se tem algum onibus que nao saiu naquela hora
def simula_saidas(linhas, saidas, num_frota):

    onibus_ativos = [(0, [0, 0, 0], 0)]
    onibus_disponiveis = num_frota
    chegadas = []
    ultima_saida = 0
    state = State(onibus_disponiveis, onibus_ativos, chegadas)
    
    for saida in saidas:
        partida_prevista = saida.horario
        saida.horario = max(ultima_saida, saida.horario)

        novos_onibus = verifica_chegadas(saida.horario, state)

        if state.onibus_disponiveis == 0:

            proxima_chegada = state.chegadas[0].horario
            if proxima_chegada // 60 > saida.horario // 60:
                print('Erro na linha ' + str(saida.linha) + ' em ' + formata_hora(partida_prevista))

            atrasa_saida(saida, proxima_chegada, state)

        ultima_saida = saida.horario

        handle_saida(linhas, saida, state)

    return state.onibus_ativos

def dados_por_minuto(dados):
    minutos = []
    i_dados = 0
    for minuto_atual in range(1, 60*24):
        if i_dados+1 < len(dados):
            proximo_minuto = dados[i_dados+1][0]
            if minuto_atual >= proximo_minuto:
                i_dados += 1
        minutos.append((minuto_atual, dados[i_dados][1], dados[i_dados][2]))
    return minutos

def plot_dados(dados):
    dados = dados_por_minuto(dados)
    dados_x = list(map(lambda x: x[0], dados))
    dados_l1 = list(map(lambda x: x[1][0], dados))
    dados_l2 = list(map(lambda x: x[1][1], dados))
    dados_l3 = list(map(lambda x: x[1][2], dados))
    dados_total = list(map(lambda x: x[2], dados))

    fig = plt.figure(figsize=(16,9), dpi=100)
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    ax.plot(dados_x, dados_l1, 'r', dados_x, dados_l2, 'g', dados_x, dados_l3, 'b', dados_x, dados_total, 'k')

    ax.set_xticks(range(0, 1441, 60))
    ax.set_xticklabels([f'{i:2}:00' for i in range(25)])

    max_total = max(dados_total)
    ax.set_yticks(range(0, max_total + 1, 2))
    ax.set_yticklabels(range(0, max_total + 1, 2))

    plt.show()

# Classes

class Linha:
    def __init__(self, id, horarios_de_saida, media):
        self.id = id
        self.horarios_de_saida = horarios_de_saida
        self.media = media

class MediaPercurso:
    def __init__(self, media_por_horario):
        self.media_por_horario = media_por_horario
    
    def em(self, horario):
        horarios_iniciais = list(map(lambda x: x[0], self.media_por_horario))
        index = bisect_left(horarios_iniciais, horario)
        if index == len(horarios_iniciais) or horarios_iniciais[index] != horario:
            index = index-1
        return self.media_por_horario[index][1]

class Evento:
    def __init__(self, linha, horario):
        self.linha = linha
        self.horario = horario
    def __eq__(self, other):
        return self.horario == other.horario and self.linha == other.linha
    def __lt__(self, other):
        if (self.horario == other.horario):
            return self.linha < other.linha
        return self.horario < other.horario
    def __repr__(self):
        return '(' + self.linha + ', ' + str(self.horario) + ')'

class State:

    def __init__(self, onibus_disponiveis, onibus_ativos, chegadas):
        self.onibus_disponiveis = onibus_disponiveis
        self.onibus_ativos = onibus_ativos
        self.chegadas = chegadas


# Simulacao

def main():
    SIMULACAO = sys.argv[1].upper()

    print("SIMULANDO MODELO " + SIMULACAO)

    if SIMULACAO == "UNIFORME":
        linhas = cria_linhas_uniforme()
    elif SIMULACAO == "SPTRANS":
        linhas = cria_linhas_sptrans()
    saidas = cria_eventos_saidas(linhas)

    dados = simula_saidas(linhas, saidas, 24)

    horario_dados = list(map(lambda x: x[0], dados))
    horario_ordenados = sorted(horario_dados)
    for i in range(0,len(dados)):
        assert dados[i][0] == horario_ordenados[i]

    plot_dados(dados)

    # Plot: ônibus por linha com ônibus como infinitos (entender picos)

if __name__ == "__main__":
    main()
