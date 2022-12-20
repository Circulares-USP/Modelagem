from verification import Evento

class LinhaRota():
    def __init__(self, linha, rota):
        self.linha = linha
        self.rota = rota

class Rota():
    def __init__(self, ida, volta=None):
        self.ida = ida
        self.volta = volta

def cria_eventos_saidas(linhas_rotas):
    saidas = []
    for id, linha_rota in linhas_rotas.items():
        saidas += list(map(lambda n: Evento(id, n), linha_rota.linha.horarios_de_saida))
    saidas.sort()
    return saidas

def trata_demanda_percentual(demanda, porc):
    for dia in demanda:
        for horario in demanda[dia]:
            for ponto in demanda[dia][horario]:
                demanda[dia][horario][ponto] = round(demanda[dia][horario][ponto] * porc)

def remove_demanda_inexistente(demanda):
    for dia in demanda:
        for horario in demanda[dia]:
            lista_pontos_delete = []
            for ponto in demanda[dia][horario]:
                if demanda[dia][horario][ponto] == {}:
                    lista_pontos_delete.append(ponto)
            for ponto in lista_pontos_delete:
                del demanda[dia][horario][ponto]

def junta_demanda(demanda1, demanda2):
    def set_from_lists(l1, l2):
        s = set(l1)
        s.update(l2)
        return s

    demanda_total = {}
    for dia in set_from_lists(demanda1.keys(), demanda2.keys()):
        demanda_total[dia] = {}
        for horario in set_from_lists(demanda1.get(dia, {}).keys(), demanda2.get(dia, {}).keys()):
            demanda_total[dia][horario] = {}
            for ponto in set_from_lists(demanda1.get(dia, {}).get(horario, {}).keys(), demanda2.get(dia, {}).get(horario, {}).keys()):
                demanda_total[dia][horario][ponto] = demanda1.get(dia, {}).get(horario, {}).get(ponto, 0) + demanda2.get(dia, {}).get(horario, {}).get(ponto, 0)
    return demanda_total

def soma_demanda(demanda):
    soma = {}
    for dia in demanda.keys():
        soma[dia] = {}
        for horario in demanda[dia].keys():
            soma[dia][horario] = 0
            for ponto in demanda[dia][horario].keys():
                soma[dia][horario] += demanda[dia][horario][ponto]
    return soma

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
        if (ponto not in demanda):
            continue
        frequencia = porc_de_linha_desce_em_ponto(ponto, rota, demanda)
        demanda[ponto] -= pessoas * frequencia
        if demanda[ponto] < 0:
            demanda[ponto] = 0

def porc_de_linha_desce_em_ponto(ponto_alvo, rota, demanda):
    sum_pessoas = 0
    for ponto in demanda:
        if ponto in rota:
            sum_pessoas += demanda[ponto]
    if sum_pessoas == 0:
        return 0
    return demanda[ponto_alvo] / sum_pessoas

def porcentagem_chegada_por_ponto(demanda_total, demanda_restante):
    atendimento = {}
    for dia in demanda_total:
        atendimento[dia] = {}
        for horario in demanda_total[dia]:
            atendimento[dia][horario] = {}
            for ponto in demanda_total[dia][horario]:
                if demanda_total[dia][horario][ponto] == 0:
                    atendimento[dia][horario][ponto] = 1
                else:
                    atendimento[dia][horario][ponto] = 1 - (demanda_restante[dia][horario][ponto] / demanda_total[dia][horario][ponto])
    return atendimento

def porcentagem_chegada_total(soma_total, soma_restante):
    porcentagem = {}
    for dia in soma_total.keys():
        porcentagem[dia] = {}
        for horario in soma_total[dia].keys():
            if soma_total[dia][horario] == 0:
                porcentagem[dia][horario] = 1
            else:
                porcentagem[dia][horario] = 1 - soma_restante[dia][horario]/soma_total[dia][horario]
    return porcentagem

def porcentagem_geral_dias(porc_dias_horarios):
    sum = {}
    for dia in porc_dias_horarios:
        for horario in porc_dias_horarios[dia]:
            if horario not in sum:
                sum[horario] = 0
            sum[horario] += porc_dias_horarios[dia][horario]

    mean = {}
    for horario in sum:
        mean[horario] = sum[horario] / len(porc_dias_horarios)

    return mean

def porcentagem_geral_dias_por_ponto(porc_dias_horarios):
    sum = {}
    amount = {}
    for dia in porc_dias_horarios:
        for horario in porc_dias_horarios[dia]:
            if horario not in sum:
                sum[horario] = {}
                amount[horario] = {}
            for ponto in porc_dias_horarios[dia][horario]:
                if ponto not in sum[horario]:
                    sum[horario][ponto] = 0
                    amount[horario][ponto] = 0
                sum[horario][ponto] += porc_dias_horarios[dia][horario][ponto]
                amount[horario][ponto] += 1

    mean = {}
    for horario in sum:
        mean[horario] = {}
        for ponto in sum[horario]:
            mean[horario][ponto] = sum[horario][ponto] / amount[horario][ponto]

    return mean


# Simulacao

class Demanda():
    def __init__(self, ida_butanta, ida_p3, volta_butanta, volta_p3):
        self.ida_butanta = ida_butanta
        self.ida_p3 = ida_p3
        self.volta_butanta = volta_butanta
        self.volta_p3 = volta_p3

class ResultadoSimulacao():
    def __init__(self, total_ida_manha, total_ida_tarde, total_volta_tarde, total_ida_manha_ponto, total_ida_tarde_ponto, total_volta_tarde_ponto):
        self.total_ida_manha = total_ida_manha
        self.total_ida_tarde = total_ida_tarde
        self.total_volta_tarde = total_volta_tarde
        self.total_ida_manha_ponto = total_ida_manha_ponto
        self.total_ida_tarde_ponto = total_ida_tarde_ponto
        self.total_volta_tarde_ponto = total_volta_tarde_ponto

def simula(demanda, linhas_rotas):
    # saidas
    saidas = cria_eventos_saidas(linhas_rotas)

    # simulacao ida
    demanda_ida_completa = junta_demanda(demanda.ida_butanta, demanda.ida_p3)
    total_ida = soma_demanda(demanda_ida_completa)
    calcula_atendimento_ida(linhas_rotas, demanda.ida_butanta, demanda.ida_p3, saidas)
    demanda_ida_restante = junta_demanda(demanda.ida_butanta, demanda.ida_p3)
    restante_ida = soma_demanda(demanda_ida_restante)
    porc_atendimento_ida = porcentagem_chegada_total(total_ida, restante_ida)
    porc_atendimento_ida_ponto = porcentagem_chegada_por_ponto(demanda_ida_completa, demanda_ida_restante)

    # simulacao volta
    demanda_volta_completa = junta_demanda(demanda.volta_butanta, demanda.volta_p3)
    total_volta = soma_demanda(demanda_volta_completa)
    calcula_atendimento_volta(linhas_rotas, demanda.volta_butanta, demanda.volta_p3, saidas)
    demanda_volta_restante = junta_demanda(demanda.volta_butanta, demanda.volta_p3)
    restante_volta = soma_demanda(demanda_volta_restante)
    porc_atendimento_volta = porcentagem_chegada_total(total_volta, restante_volta)
    porc_atendimento_volta_ponto = porcentagem_chegada_por_ponto(demanda_volta_completa, demanda_volta_restante)

    # totais
    total_ida = porcentagem_geral_dias(porc_atendimento_ida)
    total_ida_manha = total_ida[min(total_ida.keys())]
    total_ida_tarde = total_ida[max(total_ida.keys())]
    total_volta = porcentagem_geral_dias(porc_atendimento_volta)
    total_volta_tarde = total_volta[list(total_volta.keys())[0]]

    total_ida_ponto = porcentagem_geral_dias_por_ponto(porc_atendimento_ida_ponto)
    total_ida_manha_ponto = total_ida_ponto[min(total_ida_ponto.keys())]
    total_ida_tarde_ponto = total_ida_ponto[max(total_ida_ponto.keys())]
    total_volta_ponto = porcentagem_geral_dias_por_ponto(porc_atendimento_volta_ponto)
    total_volta_tarde_ponto = total_volta_ponto[list(total_volta_ponto.keys())[0]]

    return ResultadoSimulacao(total_ida_manha, total_ida_tarde, total_volta_tarde, total_ida_manha_ponto, total_ida_tarde_ponto, total_volta_tarde_ponto)
