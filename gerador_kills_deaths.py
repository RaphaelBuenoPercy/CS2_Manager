import pandas as pd
import random
from typing import List, Dict, Any, Tuple

# ==============================================================================
# 1. CARREGAMENTO E PREPARAÇÃO DOS DADOS (MODIFICADO)
# ==============================================================================

# Pesos para as funções (roles) - Mantido como antes
ROLE_WEIGHTS = {
    'kill': {
        'Entry': 1.5,
        'AWP': 1.4,
        'Ponta': 1.0,
        'Rifler': 1.2,
    },
    'death': {
        'Entry': 1.6,
        'AWP': 1.0,
        'Ponta': 0.8,
        'Rifler': 1.1,
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
    
def simular_kills_do_round(time_vencedor: str, jogadores_ct: List[Dict], jogadores_tr: List[Dict]):

    vencedores, perdedores = (jogadores_ct, jogadores_tr) if time_vencedor == "ct" else (jogadores_tr, jogadores_ct)

    kills_vencedor = random.choice([4, 5]) if random.random() < 0.85 else random.randint(1, 3)

    max_kills_perdedor = min(kills_vencedor - 1, 5) if kills_vencedor > 0 else 0

    kills_perdedor = random.randint(0, max_kills_perdedor) if random.random() < 0.91 else random.randint(kills_vencedor, 5)

    pesos_kill_vencedores = [p['over'] * ROLE_WEIGHTS['kill'].get(p['role'], 1.0) for p in vencedores]
    pesos_death_perdedores = [ROLE_WEIGHTS['death'].get(p['role'], 1.0) / p['over'] for p in perdedores]

    pesos_kill_perdedores = [p['over'] * ROLE_WEIGHTS['kill'].get(p['role'], 1.0) for p in perdedores]
    pesos_death_vencedores = [ROLE_WEIGHTS['death'].get(p['role'], 1.0) / p['over'] for p in vencedores]

    if kills_vencedor > 0 and sum(pesos_kill_vencedores) > 0:
        for jogador in random.choices(vencedores, weights=pesos_kill_vencedores, k=kills_vencedor): jogador['kills'] += 1

    if kills_perdedor > 0 and sum(pesos_kill_perdedores) > 0:
        for jogador in random.choices(perdedores, weights=pesos_kill_perdedores, k=kills_perdedor): jogador['kills'] += 1

    if kills_perdedor > 0 and sum(pesos_death_vencedores) > 0:
        for jogador in random.choices(vencedores, weights=pesos_death_vencedores, k=kills_perdedor): jogador['deaths'] += 1

    if kills_vencedor > 0 and sum(pesos_death_perdedores) > 0:
        for jogador in random.choices(perdedores, weights=pesos_death_perdedores, k=kills_vencedor): jogador['deaths'] += 1



def simular_partida(time1_nome: str, time2_nome: str, mapa: str, df_jogadores: pd.DataFrame):
    print(f"⚔️ Começando a partida: {time1_nome} vs {time2_nome} no mapa {mapa} ⚔️\n")
    try:
        time1_jogadores = obter_time(time1_nome, df_jogadores)
        time2_jogadores = obter_time(time2_nome, df_jogadores)
    except ValueError as e:
        print(f"Erro ao montar a partida: {e}")
        return
        
    print(f"--- PRIMEIRO HALF: {time1_nome} de CT e {time2_nome} de TR ---")
    pontos_t1_h1, pontos_t2_h1 = jogar_half(time1_nome, time2_nome, time1_jogadores, time2_jogadores, mapa, 12, 13, 0, 0)
    print(f"\nPlacar do 1º Half: {time1_nome} {pontos_t1_h1} x {pontos_t2_h1} {time2_nome}\n")

    if pontos_t1_h1 >= 13 or pontos_t2_h1 >= 13:
        placar_final_t1, placar_final_t2 = pontos_t1_h1, pontos_t2_h1
    else:
        print(f"--- SEGUNDO HALF: {time2_nome} de CT e {time1_nome} de TR ---")
        pontos_t2_h2, pontos_t1_h2 = jogar_half(time2_nome, time1_nome, time2_jogadores, time1_jogadores, mapa, 12, 13, pontos_t2_h1, pontos_t1_h1)
        placar_final_t1 = pontos_t1_h1 + pontos_t1_h2
        placar_final_t2 = pontos_t2_h1 + pontos_t2_h2
        
    print("\n" + "="*40 + "\n🎉 FIM DE JOGO! 🎉")
    print(f"Placar Final: {time1_nome} {placar_final_t1} x {placar_final_t2} {time2_nome}")
    print("="*40 + "\n")
    print(f"📊 Estatísticas Finais - {time1_nome}:")
    for p in sorted(time1_jogadores, key=lambda x: x['kills'], reverse=True):
        print(f" - {p['nome']:<12} | K: {p['kills']:<3} D: {p['deaths']:<3} | +/-: {p['kills'] - p['deaths']:<3} | Role: {p['role']}")
    print(f"\n📊 Estatísticas Finais - {time2_nome}:")
    for p in sorted(time2_jogadores, key=lambda x: x['kills'], reverse=True):
        print(f" - {p['nome']:<12} | K: {p['kills']:<3} D: {p['deaths']:<3} | +/-: {p['kills'] - p['deaths']:<3} | Role: {p['role']}")

# ==============================================================================
# 4. PONTO DE ENTRADA DA EXECUÇÃO (MODIFICADO)
# ==============================================================================

if __name__ == "__main__":
    # Define o nome do arquivo CSV que será lido
    arquivo_csv_jogadores = 'jogadores.csv'
    
    # 1. Carrega todos os jogadores do arquivo CSV
    df_jogadores = carregar_jogadores_de_arquivo(arquivo_csv_jogadores)
    
    # 2. Se o DataFrame foi carregado com sucesso, execute a simulação
    if df_jogadores is not None:
        simular_partida(
            time1_nome="Spirit", 
            time2_nome="Vitality", 
            mapa="Mirage", 
            df_jogadores=df_jogadores
        )