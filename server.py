from fastapi import FastAPI
from verification_demand import simula
from verification_demand import cria_linhas_sptrans

app = FastAPI()

@app.post("/")
async def simulate_buses():
    total_ida_manha, total_ida_tarde, total_volta_tarde, total_ida_manha_ponto, total_ida_tarde_ponto, total_volta_tarde_ponto = simula(cria_linhas_sptrans())

    # média de porcentagens da demanda total entregue e por ponto
    return {
        'media-total': {
            'ida-manha': total_ida_manha,
            'ida-tarde': total_ida_tarde,
            'volta-tarde': total_volta_tarde,
        },
        'media-por-ponto': {
            'ida-manha': total_ida_manha_ponto,
            'ida-tarde': total_ida_tarde_ponto,
            'volta-tarde': total_volta_tarde_ponto,
        }
    }
