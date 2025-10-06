import random
import csv
from typing import List, Dict
import re
import pandas as pd
from funcoes_simulacao_deepseek import jogar_partida, ResultadoPartida
from collections import defaultdict

def obter_opcao_numerica(min_val: int, max_val: int) -> int:
    """Valida entradas numéricas do menu"""
    while True:
        try:
            escolha = int(input("\nEscolha uma opção: ").strip())
            if min_val <= escolha <= max_val:
                return escolha
            print(f"Erro: Digite um número entre {min_val} e {max_val}")
        except ValueError:
            print("Erro: Entrada inválida. Digite apenas números!")

def listar_times_disponiveis(times: List[str]) -> None:
    """Lista todos os times disponíveis para seleção.
    
    Args:
        times: Lista de nomes dos times cadastrados
    """
    print("\nTimes disponíveis:")
    for i, time in enumerate(times, 1):
        print(f"{i}. {time}")

def validar_input_numerico(mensagem: str, tipo=int, min_val: int = None, max_val: int = None):
    """Valida entradas numéricas do usuário de forma segura.
    
    Args:
        mensagem: Texto exibido para o usuário
        tipo: Tipo numérico esperado (int/float)
        min_val: Valor mínimo permitido
        max_val: Valor máximo permitido
    
    Returns:
        Valor numérico validado
    
    Raises:
        ValueError: Se input for inválido ou fora dos limites
    """
    while True:
        try:
            valor = tipo(input(mensagem).strip())
            if min_val is not None and valor < min_val:
                raise ValueError(f"Valor deve ser ≥ {min_val}")
            if max_val is not None and valor > max_val:
                raise ValueError(f"Valor deve ser ≤ {max_val}")
            return valor
        except ValueError:
            print("Entrada inválida. Digite um número válido.")

def selecionar_times(times: List[str], num_times: int) -> List[str]:
    """Permite a seleção de times participantes do torneio.
    
    Args:
        times: Lista completa de times disponíveis
        num_times: Número de times a serem selecionados
    
    Returns:
        Lista com os times selecionados
    
    Raises:
        ValueError: Se números forem inválidos ou quantidade incorreta
    """
    listar_times_disponiveis(times)
    print(f"\nSelecione {num_times} times:")

    while True:
        try:
            escolhas = input("Digite os números separados por espaço: ").split()
            if len(escolhas) != num_times:
                raise ValueError(f"Selecione exatamente {num_times} times")
            
            indices = [int(e) for e in escolhas]
            if any(e < 1 or e > len(times) for e in indices):
                raise ValueError("Números fora do intervalo válido")
            
            print([times[i-1] for i in indices])

            return[times[i-1] for i in indices]
        
        except ValueError as e:
            print(f"Erro: {e}. Tente novamente.")

def validar_num_grupos(times: List[str], num_grupos: int) -> int:
    """Valida se o número de grupos é compatível com a quantidade de times.
    
    Args:
        times: Lista de times selecionados
        num_grupos: Número de grupos proposto
    
    Returns:
        Número de grupos validado
    """
    while len(times) % num_grupos != 0:
        print(f"Não é possível dividir {len(times)} times em {num_grupos} grupos iguais")
        num_grupos = validar_input_numerico("Novo número de grupos: ", min_val=1, max_val=len(times))
    return num_grupos

def sortear_grupos(times: List[str], num_grupos: int) -> List[List[str]]:
    """Sorteia os times em grupos aleatórios.
    
    Args:
        times: Lista de times participantes
        num_grupos: Número de grupos desejado
    
    Returns:
        Lista de grupos com distribuição aleatória
    """
    random.shuffle(times)
    return [times[i::num_grupos] for i in range(num_grupos)]

def exibir_grupos(grupos: List[List[str]]) -> None:
    """Exibe os grupos formatados na tela.
    
    Args:
        grupos: Lista de grupos a serem exibidos
    """
    print("\nGrupos Sorteados:\n")
    for i, grupo in enumerate(grupos, 1):
        print(f"Grupo {i}: {', '.join(grupo)}\n")
    print("\n")

def realizar_jogo_dbelim(time1: str, time2: str, rodada: int, chave: str, resultados: List[dict]) -> ResultadoPartida:
    """
    Realiza um jogo entre dois times e retorna o vencedor e o perdedor.
    Adiciona o resultado à lista de resultados.
    """
    print(f"\nJogo entre: {time1} e {time2}!\n")
    print("Modos de partida")
    print("1. Partida Rápida (Aleatória)")
    print("2. Partida Personalizada")

    escolha = obter_opcao_numerica(1, 2)

    if escolha == 1:
        resultado = jogar_partida(modo='auto', time1=time1, time2=time2, fase_torneio=rodada)
    elif escolha == 2:
        resultado = jogar_partida(modo='manual', time1=time1, time2=time2, fase_torneio=rodada)
    else:
        raise ValueError("Escolha inválida!")

    # Adiciona o resultado à lista de resultados
    resultados.append({
        "rodada": rodada,
        "chave": chave,
        "time1": time1,
        "time2": time2,
        "vencedor": resultado.vencedor,
        "perdedor": resultado.perdedor
    })

    return resultado

def fase_grupos(times: List[str], num_grupos: int, num_classificados: int, ida_e_volta: bool) -> tuple:
    """Executa a fase de grupos do torneio.
    
    Args:
        times: Lista de times participantes
        num_grupos: Número de grupos
        num_classificados: Times classificados por grupo
        ida_e_volta: Se True, jogos de ida e volta
    
    Returns:
        Tuple: (Lista de classificados, Lista de resultados)
    """
    grupos = sortear_grupos(times, num_grupos)
    exibir_grupos(grupos)
    
    classificados = []
    resultados = []
    
    for grupo in grupos:
        placares = {time: 0 for time in grupo}
        
        # Simula todas as combinações de partidas
        for i in range(len(grupo)):
            for j in range(i+1, len(grupo)):
                time1, time2 = grupo[i], grupo[j]
                
                # Jogos de ida e volta
                for _ in range(2 if ida_e_volta else 1):
                    print(f"\nJogo entre: {time1} e {time2}!\n")
                    print("Modos de partida")
                    print("1. Partida Rápida (Aleatória)")
                    print("2. Partida Personalizada")
        
                    escolha = obter_opcao_numerica(1, 2)
        
                    if escolha == 1:
                        resultado = jogar_partida(modo='auto', time1=time1, time2=time2, fase_torneio="Grupos")
                        placares[resultado.vencedor] += 3
                        resultados.append(resultado)

                    elif escolha == 2:
                        if time1 in times and time2 in times:
                            resultado = jogar_partida(modo='manual', time1=time1, time2=time2, fase_torneio="Grupos")
                            placares[resultado.vencedor] += 3
                            resultados.append(resultado)
                        else:
                            print("Times inválidos!")
        
        # Classificação por pontos
        grupo_ordenado = sorted(placares.items(), key=lambda x: -x[1])
        classificados.extend([time for time, _ in grupo_ordenado[:num_classificados]])
    
    return classificados, resultados

def fase_double_elimination(times: List[str], resultados: List[dict]) -> tuple[List[str], List[dict]]:
    
    """Executa uma chave de eliminação dupla."""
    vencedores = []
    perdedores = []
    rodada = 1
    random.shuffle(times)

    # Fase inicial (todos os times começam na chave de vencedores)
    while len(times) > 1:
        print(f"\n--- Rodada {rodada} ---")
        novos_vencedores = []
        novos_perdedores = []

        # Jogos na chave de vencedores
        for i in range(0, len(times), 2):
            if i + 1 < len(times):
                time1 = times[i]
                time2 = times[i + 1]
                resultado = realizar_jogo_dbelim(time1, time2, rodada, "vencedores", resultados)
                resultados.append(resultado)
                novos_vencedores.append(resultado.vencedor)
                novos_perdedores.append(resultado.perdedor)

        # Jogos na chave de perdedores (se houver times na chave de perdedores)
        if perdedores:
            novos_perdedores_chave = []
            for i in range(0, len(perdedores), 2):
                if i + 1 < len(perdedores):
                    time1 = perdedores[i]
                    time2 = perdedores[i + 1]
                    resultado = realizar_jogo_dbelim(time1, time2, rodada, "vencedores", resultados)
                    resultados.append(resultado)
                    novos_perdedores_chave.append(resultado.vencedor)

            perdedores = novos_perdedores_chave

        # Atualiza as listas de vencedores e perdedores
        vencedores = novos_vencedores
        perdedores.extend(novos_perdedores)
        times = vencedores
        rodada += 1
        random.shuffle(vencedores)
        random.shuffle(perdedores)

    # Final: o último vencedor da chave de vencedores enfrenta o último vencedor da chave de perdedores
    if perdedores:
        print(perdedores)
        print("\n--- Final Lower ---")

        resultado = realizar_jogo_dbelim(perdedores[0], perdedores[1], rodada, "vencedores", resultados)
        resultados.append(resultado)

        print("\n--- Final ---")
        resultado = realizar_jogo_dbelim(vencedores[0], resultado.vencedor, rodada, "vencedores", resultados)
        resultados.append(resultado)
        
        return resultado.vencedor, resultados
    
    else:
        return vencedores, resultados

def fase_mata_mata(times: List[str], resultados: List[Dict]) -> tuple:
    """Executa a fase eliminatória do torneio.
    
    Args:
        times: Lista de times classificados
        resultados: Lista para armazenar resultados
    
    Returns:
        Tuple: (Lista com campeão, Resultados atualizados)
    
    Raises:
        ValueError: Se número de times não for potência de 2
    """
    if (len(times) & (len(times)-1)) != 0:
        raise ValueError("Número de times deve ser potência de 2 para mata-mata")
    
    fases = {2: "Final", 4: "Semifinal", 8: "Quartas", 16: "Oitavas"}
    
    while len(times) > 1:
        fase_atual = fases.get(len(times), f"Fase com {len(times)} times")
        print(f"\n{fase_atual}:")
        
        novos_times = []
        random.shuffle(times)
        for i in range(0, len(times), 2):
            time1, time2 = times[i], times[i+1]
            print(f"\nJogo entre: {time1} e {time2}!\n")
            print("Modos de partida")
            print("1. Partida Rápida (Aleatória)")
            print("2. Partida Personalizada")
            escolha = obter_opcao_numerica(1, 2)

            if escolha == 1:
                resultado = jogar_partida(modo='auto', time1=time1, time2=time2, fase_torneio=fase_atual)

            elif escolha == 2:
                if len(times) >= 2:
                    if time1 in times and time2 in times:
                        resultado = jogar_partida(modo='manual', time1=time1, time2=time2, fase_torneio=fase_atual)
                    else:
                        print("Times inválidos!")
                else:
                    print("Necessário pelo menos 2 times registrados!")

            resultados.append(resultado)
            novos_times.append(resultado.vencedor)
            print(f"{time1} vs {time2} → {resultado.vencedor}")
        
        times = novos_times
    
    return times, resultados

def salvar_resultados_times_csv(nome_torneio: str, resultados: List[Dict]) -> None:
    """Salva os resultados do torneio em arquivo CSV, com uma linha para cada mapa."""
    resultados_dict = [resultado for resultado in resultados]

    try:
        linhas_csv = []

        for resultado in resultados_dict:
            partida_id = resultado.get("partida_id")
            fase = resultado.get("fase")
            mapas = resultado.get("mapas", [])

            for mapa_str in mapas:
                # Usando regex para extrair os dados do mapa
                pattern = r"ResultadoMapa\(mapa='([^']+)', time_ct='([^']+)', time_tr='([^']+)', placar_time1=(\d+), placar_time2=(\d+), rounds_extra=(\d+)"
                match = re.match(pattern, mapa_str)

                if match:
                    nome_mapa = match.group(1)
                    time_ct = match.group(2)
                    time_tr = match.group(3)
                    placar_time1 = int(match.group(4))
                    placar_time2 = int(match.group(5))

                    # Cria uma nova linha para o CSV
                    linha = {
                        "partida_id": partida_id,
                        "time1": time_ct,
                        "time2": time_tr,
                        "placar_time1": placar_time1,
                        "placar_time2": placar_time2,
                        "mapas": nome_mapa,
                        "fase": fase
                    }

                    linhas_csv.append(linha)
                else:
                    print(f"Formato inválido para o mapa: {mapa_str}")

        # Escreve os dados no arquivo CSV
        with open(f"{nome_torneio}_resultados.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=[
                "partida_id", "time1", "time2", "placar_time1", "placar_time2", "mapas", "fase"
            ])
            writer.writeheader()
            writer.writerows(linhas_csv)

        print(f"\nResultados salvos em {nome_torneio}_resultados.csv")

    except Exception as e:
        print(f"Erro ao salvar resultados: {str(e)}")

def salvar_estatisticas_torneio(resultados_partidas, ranking_times, nome_torneio):
    """
    Salva as estatísticas detalhadas de cada jogador em todas as partidas e mapas do torneio.
    Cada linha do CSV representa o desempenho de um jogador em um mapa específico.
    """

    estatisticas_jogadores = []
    vitorias_times = defaultdict(int)
    derrotas_times = defaultdict(int)
    for partida in resultados_partidas:
        if hasattr(partida, "mapas"):
            # Considera vencedor da partida como quem ganhou mais mapas
            v_time1 = sum(1 for m in partida.mapas if m.placar_time1 > m.placar_time2)
            v_time2 = sum(1 for m in partida.mapas if m.placar_time2 > m.placar_time1)
            vencedor = partida.mapas[0].time_ct if v_time1 > v_time2 else partida.mapas[0].time_tr
            perdedor = partida.mapas[0].time_tr if vencedor == partida.mapas[0].time_ct else partida.mapas[0].time_ct
            vitorias_times[vencedor] += 1
            derrotas_times[perdedor] += 1

    for i, partida in enumerate(resultados_partidas, start=1):
        # Cada "partida" pode conter múltiplos mapas (caso melhor de 3, por exemplo)
        if hasattr(partida, "mapas"):
            mapas = partida.mapas

        else:
            mapas = [partida]  # Compatível se só houver um mapa

        for mapa in mapas:
            # Verifica se há estatísticas salvas no ResultadoMapa
            if not hasattr(mapa, "estatisticas_jogadores"):
                print(f"Aviso: mapa {mapa.mapa} não possui estatísticas de jogadores.")
                continue

            for jogador in mapa.estatisticas_jogadores:
                stats_mapa = jogador["estatisticas"]["mapas"].get(mapa.mapa, {"kills":0,"deaths":0, "rounds":0})
                kills = stats_mapa.get("kills", 0)
                deaths = stats_mapa.get("deaths", 0)
                rounds = stats_mapa.get("rounds", 0)

                time_jogador = jogador["time"]
                time_oponente = mapa.time_tr if time_jogador == mapa.time_ct else mapa.time_ct

                estatisticas_jogadores.append({
                    "TorneioPartidaID": i,
                    "Fase": mapa.fase,
                    "Mapa": mapa.mapa,
                    "TimeCT": mapa.time_ct,
                    "TimeTR": mapa.time_tr,
                    "Oponente": time_oponente,
                    "PlacarFinal": f"{mapa.placar_time1}-{mapa.placar_time2}",
                    "Jogador": jogador["nome"],
                    "Time": jogador["time"],
                    "Kills": kills,
                    "Deaths": deaths,
                    "K/D": round(kills / max(1, deaths), 2),
                    "Rounds": rounds,
                    "KPR": round(kills / max(1, rounds), 2),
                    "DPR": round(deaths / max(1, rounds), 2),
                    "Vitorias": vitorias_times.get(jogador["time"], 0),
                    "Derrotas": derrotas_times.get(jogador["time"], 0)
            })


    # Cria o DataFrame com todas as estatísticas
    df = pd.DataFrame(estatisticas_jogadores)

    if df.empty:
        print("⚠️ Nenhuma estatística de jogador foi registrada — nada a salvar.")
        return None

    # Reorganiza colunas
    colunas_ordenadas = [
        "TorneioPartidaID", "Fase", "Mapa", "TimeCT", "TimeTR", "Oponente", "PlacarFinal",
        "Jogador", "Time", "Kills", "Deaths", "K/D",
        "Rounds", "KPR", "DPR", "Vitorias", "Derrotas"
    ]
    df = df[colunas_ordenadas]

    # Salva o CSV
    df.to_csv(f"estatisticas_torneio_{nome_torneio}.csv", index=False, encoding="utf-8-sig")

    print(f"\n📁 Estatísticas dos jogadores por mapa salvas em: estatisticas_torneio_{nome_torneio}.csv")
    print(f"Total de registros salvos: {len(df)}")

    # Depois de salvar o CSV detalhado
    df_total = salvar_estatisticas_gerais_jogadores(df, ranking_times, nome_torneio)

    return df, df_total

import pandas as pd

def salvar_estatisticas_gerais_jogadores(df_estatisticas, ranking_times, nome_torneio):
    """
    Gera um CSV agregando as estatísticas totais de cada jogador no torneio.
    - df_estatisticas: DataFrame do torneio (um registro por mapa)
    - ranking_times: lista ordenada de times (do 1º ao último lugar)
    """

    # Garante que o DataFrame tem os campos necessários
    if df_estatisticas is None or df_estatisticas.empty:
        print("⚠️ Nenhum dado de estatísticas encontrado para gerar o resumo geral.")
        return None

    # Agrupa por jogador e time, somando as métricas numéricas
    agrupado = (
        df_estatisticas
        .groupby(["Jogador", "Time"], as_index=False)
        .agg({
            "Kills": "sum",
            "Deaths": "sum",
            "Rounds": "sum",
            "Vitorias": "max",  # mesma para todos os mapas
            "Derrotas": "max"
        })
    )

    # Calcula métricas derivadas
    agrupado["K/D"] = (agrupado["Kills"] / agrupado["Deaths"].replace(0, 1)).round(2)
    agrupado["KPR"] = (agrupado["Kills"] / agrupado["Rounds"].replace(0, 1)).round(3)
    agrupado["DPR"] = (agrupado["Deaths"] / agrupado["Rounds"].replace(0, 1)).round(3)

    # Adiciona ranking do time (1º, 2º, etc.)
    ranking_dict = {time: pos + 1 for pos, time in enumerate(ranking_times)}
    agrupado["RankingTime"] = agrupado["Time"].map(ranking_dict).fillna(len(ranking_dict) + 1).astype(int)

    # Reorganiza colunas
    colunas_ordenadas = [
        "Jogador", "Time", "Kills", "Deaths", "K/D",
        "Rounds", "KPR", "DPR", "Vitorias", "Derrotas", "RankingTime"
    ]
    agrupado = agrupado[colunas_ordenadas].sort_values(by=["RankingTime", "K/D"], ascending=[True, False])

    # Salva o CSV
    agrupado.to_csv(f"estatisticas_gerais_jogadores_{nome_torneio}", index=False, encoding="utf-8-sig")

    print(f"\n📊 Estatísticas gerais dos jogadores salvas em: estatisticas_gerais_jogadores_{nome_torneio}.csv")
    print(f"Total de jogadores salvos: {len(agrupado)}")

    return agrupado

def determinar_numero_evps(num_jogadores):
    """Determina quantos EVPs serão premiados com base no total de jogadores."""
    if num_jogadores <= 20:  # Ex: 4 times
        return 2
    elif num_jogadores <= 40: # Ex: 8 times
        return 3
    elif num_jogadores <= 80: # Ex: 16 times
        return 5
    else: # Para torneios maiores
        return 6 # Um valor padrão para mais de 80 jogadores

def calcular_mvp_e_evps(df_total):
    """
    Calcula o MVP e os EVPs do torneio com base em pontuações ponderadas distintas.

    Retorna:
    DataFrame de jogadores com as colunas 'MVP_Score' e 'EVP_Score'.
    """
    if df_total is None or df_total.empty:
        print("⚠️ DataFrame total de jogadores está vazio.")
        return None

    # Pesos para o prêmio de MVP (equilibra desempenho e sucesso do time)
    pesos_mvp = {
        "K/D": 0.35,
        "KPR": 0.25,
        "RankingTime": 0.30, # Peso alto para a vitória
        "Vitorias": 0.10
    }

    # Pesos para EVP (foco maior em desempenho individual)
    pesos_evp = {
        "K/D": 0.50,         # Peso maior para o K/D
        "KPR": 0.30,         # Peso maior para o KPR
        "RankingTime": 0.15, # Peso reduzido para o sucesso do time
        "Vitorias": 0.10
    }

    df_calculo = df_total.copy()

    # Normalizar as métricas (uma vez, pois a escala é a mesma para ambos os cálculos)
    metricas = ["K/D", "KPR", "Vitorias", "RankingTime"]
    for metrica in metricas:
        min_val = df_calculo[metrica].min()
        max_val = df_calculo[metrica].max()
        if (max_val - min_val) > 0:
            df_calculo[f"{metrica}_norm"] = (df_calculo[metrica] - min_val) / (max_val - min_val)
        else:
            df_calculo[f"{metrica}_norm"] = 0.5
    
    # Inverter o ranking normalizado (1º lugar = pontuação alta)
    df_calculo["RankingTime_norm"] = 1 - df_calculo["RankingTime_norm"]

    # Calcular os dois Scores
    df_calculo["MVP_Score"] = (
        df_calculo["K/D_norm"] * pesos_mvp["K/D"] +
        df_calculo["KPR_norm"] * pesos_mvp["KPR"] +
        df_calculo["RankingTime_norm"] * pesos_mvp["RankingTime"] +
        df_calculo["Vitorias_norm"] * pesos_mvp["Vitorias"]
    )
    
    df_calculo["EVP_Score"] = (
        df_calculo["K/D_norm"] * pesos_evp["K/D"] +
        df_calculo["KPR_norm"] * pesos_evp["KPR"] +
        df_calculo["RankingTime_norm"] * pesos_evp["RankingTime"] +
        df_calculo["Vitorias_norm"] * pesos_evp["Vitorias"]
    )

    return df_calculo

def mostrar_historico_partidas(lista_de_partidas):
    """
    Mostra o histórico de todas as partidas de um torneio, em ordem de fase.
    Funciona diretamente com a lista de objetos de partida.
    """
    if not lista_de_partidas:
        print("⚠️ Nenhuma partida encontrada para exibir o histórico.")
        return

    print("\n\n=============================================")
    print("📜 HISTÓRICO COMPLETO DAS PARTIDAS")
    print("=============================================\n")

    # 1. Definir a ordem cronológica correta das fases
    ordem_fases = ["Oitavas de Final", "Quartas de Final", "Semifinal", "Final"]
    
    # Mapeia cada fase para um número para facilitar a ordenação
    fase_mapa_ordem = {fase: i for i, fase in enumerate(ordem_fases)}

    # 2. Ordenar a lista de partidas usando o mapa de ordem
    # Usamos .get(p.fase, 99) para que fases não listadas (ex: "Rodada 1") não quebrem o código
    partidas_ordenadas = sorted(lista_de_partidas, key=lambda p: fase_mapa_ordem.get(p.fase, 99))

    # 3. Iterar pela lista ordenada e exibir os resultados
    for partida in partidas_ordenadas:
        # A 'partida' aqui é um objeto que contém uma lista de mapas (mesmo que seja só 1)
        if not hasattr(partida, 'mapas') or not partida.mapas:
            continue

        # Pega as informações gerais da partida a partir do primeiro mapa
        primeiro_mapa = partida.mapas[0]
        time1 = primeiro_mapa.time_ct
        time2 = primeiro_mapa.time_tr

        # Calcula o placar da série (contando vitórias de mapa)
        vitorias_time1 = sum(1 for m in partida.mapas if m.placar_time1 > m.placar_time2)
        vitorias_time2 = len(partida.mapas) - vitorias_time1

        # Formata o resultado final da série
        if vitorias_time1 > vitorias_time2:
            resultado_final = f"Resultado: **{time1}** {vitorias_time1} - {vitorias_time2} {time2}"
        else:
            resultado_final = f"Resultado: {time1} {vitorias_time1} - {vitorias_time2} **{time2}**"
        
        # Imprime o bloco de informações da partida
        print(f"--- {partida.fase}: {time1} vs {time2} ---")
        for mapa in partida.mapas:
            print(f"  - {mapa.mapa}: {mapa.time_ct} {mapa.placar_time1}-{mapa.placar_time2} {mapa.time_tr}")
        print(f"➡️  {resultado_final}\n")

def mostrar_resumo_torneio(df, df_total):
    """
    Mostra um resumo geral do torneio a partir dos DataFrames:
      - df: estatísticas por mapa
      - df_total: estatísticas totais por jogador no torneio
    """

    if df is None or df.empty:
        print("⚠️ DataFrame de mapas está vazio.")
        return
    if df_total is None or df_total.empty:
        print("⚠️ DataFrame total de jogadores está vazio.")
        return

    print("\n=== 🏆 RESUMO GERAL DO TORNEIO ===")

    # Calcular as pontuações de MVP e EVP
    df_premiacao = calcular_mvp_e_evps(df_total)
    
    if df_premiacao is None:
        return

    # ---------- MVP DO TORNEIO ----------
    df_premiacao_mvp = df_premiacao.sort_values(by="MVP_Score", ascending=False)
    mvp = df_premiacao_mvp.iloc[0]
    
    print("\n\n=============================================")
    print(f"🏅 O MVP DO TORNEIO É: {mvp['Jogador']} ({mvp['Time']})")
    print("=============================================\n")
    
    print("🏆 Top 5 Candidatos a MVP (baseado no MVP Score):\n")
    print(df_premiacao_mvp[[
        "Jogador", "Time", "K/D", "RankingTime", "MVP_Score"
    ]].head(5).to_string(index=False))

    # ---------- EVPs DO TORNEIO ----------
    num_jogadores = len(df_total)
    num_evps = determinar_numero_evps(num_jogadores)
    
    print(f"\n\n=============================================")
    print(f"🌟 EVPs DO TORNEIO ({num_evps} jogadores)")
    print("=============================================\n")

    # Ordenar pelo score de EVP
    df_premiacao_evp = df_premiacao.sort_values(by="EVP_Score", ascending=False)
    
    # Pegar os jogadores que não são o #1 da lista de EVP
    # Isso garante que mesmo que o MVP tenha o maior EVP score, ele não apareça aqui.
    evps = df_premiacao_evp.iloc[1:num_evps + 1]

    print(f"Jogadores com desempenho individual excepcional (baseado no EVP Score):\n")
    print(evps[[
        "Jogador", "Time", "K/D", "RankingTime", "EVP_Score"
    ]].to_string(index=False))

    # ---------- TOP 10 JOGADORES (DESEMPENHO TOTAL) ----------
    print("\n💥 Top 10 Jogadores do Torneio (por K/D total):\n")

    top10_total = (
        df_total
        .sort_values(by=["K/D", "KPR"], ascending=[False, False])
        .head(10)
        .reset_index(drop=True)
    )

    print(top10_total[[
        "Jogador", "Time", "Kills", "Deaths", "K/D",
        "Rounds", "KPR", "DPR", "Vitorias", "Derrotas", "RankingTime"
    ]].to_string(index=False))


    # ---------- TOP 10 DESEMPENHOS INDIVIDUAIS EM MAPAS ----------
    print("\n🔥 Top 10 Melhores Desempenhos em Mapas (por K/D no mapa):\n")

    top10_mapas = (
        df.sort_values(by=["K/D", "Kills"], ascending=[False, False])
        .head(10)
        .reset_index(drop=True)
    )

    print(top10_mapas[[
        "Jogador", "Time", "Oponente","Fase", "Mapa", "PlacarFinal",
        "Kills", "Deaths", "K/D", "Rounds", "KPR", "DPR"
    ]].to_string(index=False))

    return top10_total, top10_mapas

def criar_torneio(times: List[str]) -> None:
    """Fluxo principal para criação e execução do torneio."""
    if len(times) < 2:
        print("Necessário pelo menos 2 times registrados.")
        return

    try:
        nome_torneio = input("Nome do torneio: ").strip()
        num_times = validar_input_numerico(
            "Número de participantes: ", 
            min_val=2, 
            max_val=len(times)
        )
        
        times_selecionados = selecionar_times(times, num_times)
        formato = validar_input_numerico(
            "Formato (1-Grupos / 2-Mata-mata / 3-Double Elimination): ",
            min_val=1,
            max_val=3
        )

        resultados = []
        
        if formato == 1:
            num_grupos = validar_input_numerico(
                "Número de grupos: ",
                min_val=1,
                max_val=len(times_selecionados)
            )
            num_grupos = validar_num_grupos(times_selecionados, num_grupos)
            
            num_classificados = validar_input_numerico(
                "Classificados por grupo: ",
                min_val=1,
                max_val=len(times_selecionados)//num_grupos
            )
            
            ida_e_volta = validar_input_numerico(
                "Jogos de ida e volta? (1-Sim / 2-Não): ",
                min_val=1,
                max_val=2
            ) == 1
            
            classificados, resultados = fase_grupos(
                times_selecionados, 
                num_grupos, 
                num_classificados, 
                ida_e_volta
            )
            
            campeao, resultados = fase_mata_mata(classificados, resultados)
            print(f"\n🏆 Campeão: {campeao[0]} 🏆")
            salvar_resultados_times_csv(nome_torneio, resultados)

        elif formato == 3:
            campeao, resultados = fase_double_elimination(times_selecionados, resultados)
            print(f"\n🏆 Campeão: {campeao} 🏆")
            salvar_resultados_times_csv(nome_torneio, resultados)
            print("CRIAR SALVAR RESULTADOS CSV PARA DOUBLE ELIMINATION, TESTAR COM MAIS QUE 4 TIMES E CRIAR FORMATO SUIÇO")

        else:
            classificados = times_selecionados
            campeao, resultados = fase_mata_mata(classificados, resultados)
            print(f"\n🏆 Campeão: {campeao[0]} 🏆")
            salvar_resultados_times_csv(nome_torneio, resultados)

    except Exception as e:
        print(f"\nErro durante execução: {str(e)}")