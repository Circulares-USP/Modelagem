from verification import Evento

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

def id_to_nome_to_list():
    bus_stops_list = []

    for id in id_to_nome.keys():
        bus_stops_list.append({'id': id, 'nome': id_to_nome[id]})
    
    return bus_stops_list

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
                        print("xxx demanda_p3[dia][horario]: " + str(demanda_p3[dia][horario]))
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

def porcentagem_chegada_por_ponto(demanda_total, demanda_restante):
    atendimento = {}
    for dia in demanda_total:
        atendimento[dia] = {}
        for horario in demanda_total[dia]:
            atendimento[dia][horario] = {}
            for ponto in demanda_total[dia][horario]:

                soma_linhas_ponto_total = 0
                soma_linhas_ponto_restante = 0
                for linha in demanda_total[dia][horario][ponto]:
                    soma_linhas_ponto_restante += demanda_restante[dia][horario][ponto][linha]
                    soma_linhas_ponto_total += demanda_total[dia][horario][ponto][linha]

                atendimento[dia][horario][ponto] = 1 - (soma_linhas_ponto_restante / soma_linhas_ponto_total)
    return atendimento

def porcentagem_chegada_total(soma_total, soma_restante):
    porcentagem = {}
    for dia in soma_total.keys():
        porcentagem[dia] = {}
        for horario in soma_total[dia].keys():
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
        self.total_ida_manha_ponto = total_ida_manha_ponto,
        self.total_ida_tarde_ponto = total_ida_tarde_ponto,
        self.total_volta_tarde_ponto = total_volta_tarde_ponto

def simula(demanda, linhas_rotas):
    # saidas
    saidas = cria_eventos_saidas(linhas_rotas)

    # simulacao ida
    total_ida = soma_demanda(junta_demanda(demanda.ida_butanta, demanda.ida_p3))
    calcula_atendimento_ida(linhas_rotas, demanda.ida_butanta, demanda.ida_p3, saidas)
    demanda_ida_restante = junta_demanda(demanda.ida_butanta, demanda.ida_p3)
    restante_ida = soma_demanda(demanda_ida_restante)
    porc_atendimento_ida = porcentagem_chegada_total(total_ida, restante_ida)

    # simulacao volta
    total_volta = soma_demanda(junta_demanda(demanda.volta_butanta, demanda.volta_p3))
    calcula_atendimento_volta(linhas_rotas, demanda.volta_butanta, demanda.volta_p3, saidas)
    demanda_volta_restante = junta_demanda(demanda.volta_butanta, demanda.volta_p3)
    restante_volta = soma_demanda(demanda_volta_restante)
    porc_atendimento_volta = porcentagem_chegada_total(total_volta, restante_volta)

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
