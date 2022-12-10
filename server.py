from fastapi import FastAPI
from verification_demand import Demanda, simula, cria_linhas_sptrans, junta_demanda
from demanda.demanda_ida_butanta import demanda_ida_butanta
from demanda.demanda_ida_butanta_func import demanda_ida_butanta_func
from demanda.demanda_ida_p3 import demanda_ida_p3
from demanda.demanda_ida_p3_func import demanda_ida_p3_func
from demanda.demanda_volta_butanta import demanda_volta_butanta
from demanda.demanda_volta_p3 import demanda_volta_p3

app = FastAPI()

@app.post("/")
async def simulate_buses():
    demanda = get_demanda()
    resultado = simula(demanda, cria_linhas_sptrans())

    # média de porcentagens da demanda entregue por ponto
    return {
        'media-total': {
            'ida-manha': resultado.total_ida_manha,
            'ida-tarde': resultado.total_ida_tarde,
            'volta-tarde': resultado.total_volta_tarde,
        },
        'media-por-ponto': {
            # TODO: alterar para maps de id-ponto -> porcentagem
            'ida-manha': resultado.porc_atendimento_ida,
            'ida-tarde': resultado.porc_atendimento_ida,
            'volta-tarde': resultado.porc_atendimento_volta,
        }
    }

# data

def get_demanda():
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

    demanda_ida_completa_butanta = junta_demanda(demanda_ida_butanta, demanda_ida_butanta_func)
    demanda_ida_completa_p3 = junta_demanda(demanda_ida_p3, demanda_ida_p3_func)

    demanda = Demanda(demanda_ida_completa_butanta, demanda_ida_completa_p3, demanda_volta_butanta, demanda_volta_p3)
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
