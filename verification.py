from bisect import insort

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
            saidas_a_cada = 60 // num_saidas # TODO: nao completamente uniforme
            for minute in range(0, 60, saidas_a_cada):
                ret.append(60*hour + minute)
    return ret

def merge(listas):
    pass

# Classes

class Linha:
    def __init__(self, id, saidas_por_hora, media):
        self.id = id
        self.horarios_de_saida = calcular_horarios_saidas(saidas_por_hora)
        self.media = media

class Evento:
    def __init__(self, linha, horario):
        self.linha = linha
        self.horario = horario
    def __eq__(self, other):
        return self.horario == other.horario
    def __lt__(self, other):
        return self.horario < other.horario
    def __repr__(self):
        return '(' + self.linha + ', ' + str(self.horario) + ')'

# Simulacao

linhas = {
    '8012': Linha(
        '8012',
        [ 2, 1, 1, 1, 3, 5, 7, 7, 6, 6, 5, 4, 5, 7, 7, 6, 7, 6, 7, 6, 4, 5, 6, 5 ],
        75,
    ),
    '8022': Linha(
        '8022',
        [ 3, 2, 1, 1, 3, 5, 8, 8, 6, 7, 6, 6, 8, 5, 8, 8, 8, 7, 6, 7, 6, 5, 6, 4 ],
        80,
    ),
    '8032': Linha(
        '8032',
        [ 2, 0, 0, 0, 0, 2, 5, 5, 4, 4, 4, 4, 6, 5, 4, 4, 5, 5, 6, 5, 4, 4, 6, 2 ],
        35
    )
}

# TODO: Optimizavel
saidas = []
for id, linha in linhas.items():
    saidas += list(map(lambda n: Evento(id, n), linha.horarios_de_saida))
saidas.sort()

# State
onibus_disponiveis = 18
chegadas = []
ultima_saida = 0
for saida in saidas:
    horario = max(ultima_saida, saida.horario)

    ind_chegadas = 0
    while ind_chegadas < len(chegadas):
        if chegadas[ind_chegadas].horario < horario:
            onibus_disponiveis += 1
        else:
            break
        ind_chegadas += 1
    chegadas = chegadas[ind_chegadas:]

    if onibus_disponiveis == 0:
        ultima_saida = chegadas[0].horario + 1

        if ultima_saida // 60 > saida.horario // 60:
            print('Erro na linha ' + str(saida.linha) + ' em ' + str(saida.horario // 60) + ':' + str(saida.horario % 60))
            exit()

        saida.horario = ultima_saida
        chegadas = chegadas[1:]
        onibus_disponiveis += 1

    insort(chegadas, Evento(saida.linha, saida.horario + linhas[saida.linha].media))
    onibus_disponiveis -= 1

# Algoritmo:
# 1. Calcular os horários de saída
# 2. for incrementando os minutos
#    - Adiciona os onibus que chegaram
#    - Conto os onibus que precisam sair agora
#    - Se tem onibus disponivel,
#      - Decrementar os onibus disponiveis e tirar da lista dos horarios de saida e adiciona na lista de horários de chegada
#    - Se minutos % 60, verifico se tem algum onibus que nao saiu naquela hora

# Plot: ônibus por linha com ônibus como infinitos (entender picos)
