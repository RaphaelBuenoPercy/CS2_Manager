import pandas as pd
import random
from typing import List, Dict, Any, Tuple

# ==============================================================================
# 1. CARREGAMENTO E PREPARAÇÃO DOS DADOS (MODIFICADO)
# ==============================================================================

# Pesos para as funções (roles) - Mantido como antes
ROLE_WEIGHTS = {
    'kill': {
        'Entry': 1.1,
        'AWP': 1.0,
        'Ponta': 0.9,
        'Rifler': 1.0,
    },
    'death': {
        'Entry': 1.1,
        'AWP': 0.9,
        'Ponta': 0.9,
        'Rifler': 1.0,
    }
}

def carregar_jogadores_de_arquivo(caminho_do_arquivo: str) -> pd.DataFrame:
    """
    Carrega os dados dos jogadores diretamente de um arquivo CSV.
    
    Args:
        caminho_do_arquivo (str): O nome do arquivo (ex: 'jogadores.csv').
        
    Returns:
        pd.DataFrame: Um DataFrame com todos os jogadores carregados.
    """
    try:
        return pd.read_csv(caminho_do_arquivo)
    except FileNotFoundError:
        print(f"Erro: O arquivo '{caminho_do_arquivo}' não foi encontrado.")
        print("Certifique-se de que o arquivo CSV está na mesma pasta que o script.")
        return None

def obter_jogadores(nome_time: str, df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Filtra o DataFrame para obter os jogadores de um time específico e
    formata os dados para a simulação.
    """
    time_df = df[df['time'] == nome_time]
    if len(time_df) == 0:
        raise ValueError(f"Time '{nome_time}' não encontrado no CSV.")
        
    jogadores = []
    for _, row in time_df.iterrows():
        # Normaliza o 'over'. Um jogador com over 80 terá 1.0.
        over_normalizado = row['over'] / 80.0
        
        jogadores.append({
            "nome": row['nick'],
            "over": over_normalizado,
            "role": row['funcao'],
            "kills": 0,
            "deaths": 0
        })
    return jogadores

def calcular_over_medio(jogadores: List[Dict[str, Any]]) -> float:
    if not jogadores: return 0
    return sum(p['over'] for p in jogadores) / len(jogadores)
    
def simular_kills_do_round(time_vencedor: str, jogadores_ct: List[Dict], jogadores_tr: List[Dict], mapa):

    vencedores, perdedores = (jogadores_ct, jogadores_tr) if time_vencedor == "ct" else (jogadores_tr, jogadores_ct)

    kills_vencedor = random.choice([4, 5]) if random.random() < 0.85 else random.randint(1, 3)

    max_kills_perdedor = min(kills_vencedor - 1, 5) if kills_vencedor > 0 else 0

    kills_perdedor = random.randint(0, max_kills_perdedor) if random.random() < 0.91 else random.randint(kills_vencedor, 5)

    if not isinstance(vencedores, list):
        raise TypeError(f"Esperava lista de jogadores, mas recebeu: {type(vencedores)} {vencedores}")
    
    pesos_kill_vencedores = [p['over']**0.8 * ROLE_WEIGHTS['kill'].get(p['role'], 1.0) + 0.2 for p in vencedores]
    pesos_death_perdedores = [p['over']**0.8 * ROLE_WEIGHTS['death'].get(p['role'], 1.0) + 0.2 for p in perdedores]


    pesos_kill_perdedores = [p['over']**0.8 * ROLE_WEIGHTS['kill'].get(p['role'], 1.0) + 0.2 for p in perdedores]
    pesos_death_vencedores = [p['over']**0.8 * ROLE_WEIGHTS['death'].get(p['role'], 1.0) + 0.2 for p in vencedores]


 # Vencedor mata perdedor
    if kills_vencedor > 0 and sum(pesos_death_perdedores) > 0:
        mortos = random.choices(
            perdedores,
            weights=pesos_death_perdedores,
            k=min(kills_vencedor, len(perdedores))
        )
        for morto in mortos:
            registrar_death(morto, mapa)
            killer = random.choices(vencedores, weights=pesos_kill_vencedores, k=1)[0]
            registrar_kill(killer, mapa)

    # Perdedor mata vencedor
    if kills_perdedor > 0 and sum(pesos_death_vencedores) > 0:
        mortos = random.choices(
            vencedores,
            weights=pesos_death_vencedores,
            k=min(kills_perdedor, len(vencedores))
        )
        for morto in mortos:
            registrar_death(morto, mapa)
            killer = random.choices(perdedores, weights=pesos_kill_perdedores, k=1)[0]
            registrar_kill(killer, mapa)




def registrar_kill(jogador, mapa):
    if mapa not in jogador["estatisticas"]["mapas"]:
        jogador["estatisticas"]["mapas"][mapa] = {"kills": 0, "deaths": 0}
    jogador["estatisticas"]["mapas"][mapa]["kills"] += 1
    jogador["estatisticas"]["total"]["kills"] += 1

def registrar_death(jogador, mapa):
    if mapa not in jogador["estatisticas"]["mapas"]:
        jogador["estatisticas"]["mapas"][mapa] = {"kills": 0, "deaths": 0}
    jogador["estatisticas"]["mapas"][mapa]["deaths"] += 1
    jogador["estatisticas"]["total"]["deaths"] += 1



# ==============================================================================
# 4. PONTO DE ENTRADA DA EXECUÇÃO (MODIFICADO)
# ==============================================================================

if __name__ == "__main__":
    # Define o nome do arquivo CSV que será lido
    arquivo_csv_jogadores = 'jogadores.csv'
    
    # 1. Carrega todos os jogadores do arquivo CSV
    df_jogadores = carregar_jogadores_de_arquivo(arquivo_csv_jogadores)