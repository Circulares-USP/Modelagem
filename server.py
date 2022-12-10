from fastapi import FastAPI
from verification_demand import simula
from verification_demand import cria_linhas_sptrans

app = FastAPI()

@app.post("/")
async def simulate_buses():
    resultado = simula(cria_linhas_sptrans())

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
