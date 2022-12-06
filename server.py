from fastapi import FastAPI
from verification_demand import simula
from verification_demand import cria_linhas_sptrans

app = FastAPI()

@app.post("/")
async def simulate_buses():
    total_ida_manha, total_ida_tarde, total_volta_tarde, porc_atendimento_ida, porc_atendimento_volta = simula(cria_linhas_sptrans())

    # média de porcentagens da demanda entregue por ponto
    return {
        'totais': {
            'ida-manha': total_ida_manha,
            'ida-tarde': total_ida_tarde,
            'volta-tarde': total_volta_tarde,
        },
        'ida': porc_atendimento_ida,
        'volta': porc_atendimento_volta
    }
