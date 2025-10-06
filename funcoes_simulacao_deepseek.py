import csv
import random
import math
from dataclasses import dataclass
from typing import Any, List, Tuple, Dict, Literal

from colorama import Fore, Style

import pandas as pd
from estrategias_deepseek import estrategias_por_mapa, estrategia_resultado
from funcoes_prejogo_deepseek import times, vetar_e_escolher_mapas, calcular_over_medio
from gerador_kills_deaths import simular_kills_do_round, carregar_jogadores_de_arquivo, obter_jogadores

# ==================== CLASSES DE DADOS ====================
@dataclass
class ResultadoMapa:
    mapa: str
    time_ct: str
    time_tr: str
    placar_time1: int
    placar_time2: int
    rounds: int
    rounds_extra: int = 0

@dataclass
class ResultadoPartida:
    partida_id: int
    mapas: List[ResultadoMapa]
    vencedor: str = ""
    perdedor: str = ""
    modo_jogo: Literal['manual', 'semi-auto', 'auto'] = "manual"
    fase: str = ""
    def to_dict(self) -> dict:
        """Converte o objeto ResultadoPartida em um dicionário."""
        return {
            "partida_id": self.partida_id,
            "mapas": [mapa.to_dict() if hasattr(mapa, 'to_dict') else str(mapa) for mapa in self.mapas],
            "vencedor": self.vencedor,
            "perdedor": self.perdedor,
            "modo_jogo": self.modo_jogo,
            "fase": self.fase
            }

# ==================== CONTROLE DE PARTIDAS ====================
class ContadorPartidas:
    _id = 1
    
    @classmethod
    def proxima_partida(cls):
        current = cls._id
        cls._id += 1
        return current

# ==================== FUNÇÕES AUXILIARES ====================
ModoJogo = Literal['manual', 'semi-auto', 'auto']

def validar_time(nome: str) -> str:
    if nome not in times:
        raise ValueError(f"Time '{nome}' não registrado!")
    return nome

def escolher_estrategia(time: str, estrategias: List[str], modo: ModoJogo) -> int:
    """Seleção de estratégia baseada no modo de jogo"""
    print(modo)
    if modo == 'auto':
        return random.randint(0, len(estrategias)-1)
    
    if modo == 'semi-auto' and "Jogador" not in time:
        return random.randint(0, len(estrategias)-1)
    
    print(f"\n{time}, estratégias disponíveis:")
    for i, estrategia in enumerate(estrategias, 1):
        print(f"{i}. {estrategia}")
    
    while True:
        try:
            escolha = 4
            - 1
            if 0 <= escolha < len(estrategias):
                return escolha
            print("Número inválido!")
        except ValueError:
            print("Digite apenas números!")

# ==================== FUNÇÕES PRINCIPAIS ====================
def jogar_half(
    # --- Argumentos Obrigatórios ---
    time_ct: str, 
    time_tr: str, 
    jogadores_ct: List[Dict[str, Any]],
    jogadores_tr: List[Dict[str, Any]],
    mapa: str,
    modo: ModoJogo,
    # --- Argumentos Opcionais (com valor padrão) ---
    max_rounds: int = 12,
    meta: int = 13,
    pontos_iniciais_ct: int = 0,
    pontos_iniciais_tr: int = 0
) -> Tuple[int, int]:
    """Executa um half de jogo e retorna os pontos conquistados pelos lados CT e TR."""
    try:
        if mapa not in estrategias_por_mapa:
            raise ValueError(f"Mapa '{mapa}' não encontrado nas estratégias")
            
        if modo not in ModoJogo.__args__:
            raise ValueError(f"Modo de jogo inválido: {modo}")

        estrategias_ct = estrategias_por_mapa[mapa]["ct"]
        estrategias_tr = estrategias_por_mapa[mapa]["tr"]
        
        pontos_ct = 0
        pontos_tr = 0

        # Calcula o over médio dos times
        over_ct = calcular_over_medio(time_ct)
        over_tr = calcular_over_medio(time_tr)
        
        for _ in range(max_rounds):
            idx_ct = escolher_estrategia(time_ct, estrategias_ct, modo)
            idx_tr = escolher_estrategia(time_tr, estrategias_tr, modo)
            
            resultado = decidir_vencedor_round(over_ct, over_tr, "ct", idx_ct, idx_tr, mapa)

            if resultado == "ct":
                pontos_ct += 1
                print(f"{time_ct} (CT) venceu! CT {pontos_iniciais_ct + pontos_ct}-{pontos_iniciais_tr + pontos_tr} TR")
            else:
                pontos_tr += 1
                print(f"{time_tr} (TR) venceu! CT {pontos_iniciais_ct + pontos_ct}-{pontos_iniciais_tr + pontos_tr} TR")
            
            simular_kills_do_round(resultado, jogadores_ct, jogadores_tr, mapa)
            # Verifica se atingiu a meta considerando os pontos iniciais
            if (pontos_iniciais_ct + pontos_ct) >= meta or (pontos_iniciais_tr + pontos_tr) >= meta:
                break
        
        return pontos_ct, pontos_tr
    
    except KeyError as e:
        print(f"Erro de configuração: Estratégia não encontrada para o mapa {mapa}")
        raise
    except Exception as e:
        print(f"Erro durante o half: {type(e).__name__} - {str(e)}")
        raise

def jogar_mapa(time1: str, time2: str, mapa: str, modo: ModoJogo, jogadores_time1: int = 0, jogadores_time2: int = 0) -> ResultadoMapa:
    """Executa uma partida completa em um mapa"""
    
    try:
        resultado = ResultadoMapa(mapa=mapa, time_ct=time1, time_tr=time2, placar_time1=0, placar_time2=0, rounds=0)
        resetar_estatisticas_para_mapa(jogadores_time1, mapa)
        resetar_estatisticas_para_mapa(jogadores_time2, mapa)

        
        # Primeiro half (CT: time1, TR: time2)
        resultado.placar_time1, resultado.placar_time2 = jogar_half(
            time_ct=time1,
            time_tr=time2,
            jogadores_ct=jogadores_time1, # Passando a lista de jogadores para o parâmetro correto
            jogadores_tr=jogadores_time2, # Passando a lista de jogadores para o parâmetro correto
            mapa=mapa,
            modo=modo,
            # Os argumentos abaixo são opcionais, você só precisa passar se quiser mudar o padrão
            max_rounds=12,
            meta=13,
            pontos_iniciais_ct= 0,
            pontos_iniciais_tr= 0
            )

        # Segundo half (CT: time2, TR: time1) com pontos iniciais
        if resultado.placar_time1 < 13 and resultado.placar_time2 < 13:
            placar_time2_half, placar_time1_half = jogar_half(
                time_ct=time2,
                time_tr=time1,
                jogadores_ct=jogadores_time2, # Passando a lista de jogadores para o parâmetro correto
                jogadores_tr=jogadores_time1, # Passando a lista de jogadores para o parâmetro correto
                mapa=mapa,
                modo=modo,
                # Os argumentos abaixo são opcionais, você só precisa passar se quiser mudar o padrão
                max_rounds=12,
                meta=13,
                pontos_iniciais_ct= resultado.placar_time2,
                pontos_iniciais_tr= resultado.placar_time1
                )
            resultado.placar_time1 += placar_time1_half
            resultado.placar_time2 += placar_time2_half

        # Verificar empate e iniciar overtime
        if resultado.placar_time1 == resultado.placar_time2:
            overtime_count = 1
            resultado = jogar_ot(time1, time2, mapa, modo, resultado, overtime_count,
                     jogadores_time1=jogadores_time1, 
                     jogadores_time2=jogadores_time2)


        print("\n" + "="*40 + "\n🎉 FIM DE MAPA! 🎉")
        print(f"Placar Final: {time1} {resultado.placar_time1} x {resultado.placar_time2} {time2}")
        print("="*40 + "\n")   

        # Número total de rounds jogados no mapa
        rounds_total = resultado.placar_time1 + resultado.placar_time2
        resultado.rounds = rounds_total

        # Atualiza o número de rounds jogados de cada jogador
        for jogador in jogadores_time1 + jogadores_time2:
            jogador["estatisticas"]["mapas"][mapa]["rounds"] += rounds_total
            jogador["estatisticas"]["total"]["rounds"] += rounds_total

        resultado.estatisticas_jogadores = jogadores_time1 + jogadores_time2

        return resultado

    except Exception as e:
        print(f"Erro durante a execução do mapa {mapa}: {str(e)}")
        resultado.erro = True
        return resultado

def jogar_ot(time1: str, time2: str, mapa: str, modo: ModoJogo, resultado, overtime_count: int,
             jogadores_time1: List[Dict[str, Any]],
             jogadores_time2: List[Dict[str, Any]]) -> ResultadoMapa:
        
        while True:
            print(f"\n=== Overtime {overtime_count} (Placar: {resultado.placar_time1}-{resultado.placar_time2}) ===")
            
            # Jogar até 4 vitórias no overtime, alternando lados a cada 3 rounds
            placar_meta = 13 + (overtime_count * 3)  # Meta para vencer o overtime
        
            # Primeiro lado do overtime (Time 1 CT)  
            # Jogar rounds alternados até atingir 4 vitórias
            while True:
                # Primeiro Half Overtime
                placar_time1_1ot, placar_time2_1ot = jogar_half(
                time_ct=time1,
                time_tr=time2,
                jogadores_ct=jogadores_time1, # Passando a lista de jogadores para o parâmetro correto
                jogadores_tr=jogadores_time2, # Passando a lista de jogadores para o parâmetro correto
                mapa=mapa,
                modo=modo,
                # Os argumentos abaixo são opcionais, você só precisa passar se quiser mudar o padrão
                max_rounds=3,
                meta=placar_meta,
                pontos_iniciais_ct=resultado.placar_time1,
                pontos_iniciais_tr=resultado.placar_time2,
                 )
                
                resultado.placar_time1 += placar_time1_1ot
                resultado.placar_time2 += placar_time2_1ot
                
                # TR joga até 3 rounds OU até atingir 4 vitórias
                placar_time2_1ot, placar_time1_1ot = jogar_half(
                time_ct=time2,
                time_tr=time1,
                jogadores_ct=jogadores_time2, # Passando a lista de jogadores para o parâmetro correto
                jogadores_tr=jogadores_time1, # Passando a lista de jogadores para o parâmetro correto
                mapa=mapa,
                modo=modo,
                # Os argumentos abaixo são opcionais, você só precisa passar se quiser mudar o padrão
                max_rounds=3,
                meta=placar_meta,
                pontos_iniciais_ct=resultado.placar_time2,
                pontos_iniciais_tr=resultado.placar_time1,
                 )
                
                resultado.placar_time1 += placar_time1_1ot
                resultado.placar_time2 += placar_time2_1ot
                break

            # Verificar se o overtime terminou
            if resultado.placar_time1 >= placar_meta:
                print(f"{time1} venceu o overtime {resultado.placar_time1}-{resultado.placar_time2}!")
                return resultado
            elif resultado.placar_time2 >= placar_meta:
                print(f"{time2} venceu o overtime {resultado.placar_time2}-{resultado.placar_time2}!")
                return resultado
            else:
                overtime_count += 1
                return jogar_ot(time1, time2, mapa, modo, resultado, overtime_count, jogadores_time1=jogadores_time1, 
                     jogadores_time2=jogadores_time2)

def jogar_partida(
    modo: ModoJogo = 'manual',
    time1: str = None,
    time2: str = None,
    fase_torneio: str = None ) -> ResultadoPartida:
    """Gerencia uma partida completa entre dois times"""
    try:
        times_config = carregar_times_config("times.csv")
        # Validação inicial
        try:
            time1 = validar_time(time1) if time1 else random.choice(times)
            time2 = validar_time(time2) if time2 else random.choice([t for t in times if t != time1])
            jogadores_Dataframe = carregar_jogadores_de_arquivo("jogadores.csv")
            jogadores_time1 = obter_jogadores(time1, jogadores_Dataframe)
            jogadores_time2 = obter_jogadores(time2, jogadores_Dataframe)

        except (ValueError, IndexError) as e:
            raise RuntimeError(f"Seleção de times inválida: {str(e)}")

        resultado = ResultadoPartida(
            partida_id=ContadorPartidas.proxima_partida(),
            mapas=[],
            modo_jogo=modo,
            fase = fase_torneio
        )

        print(f"\n=== PARTIDA {resultado.partida_id} ===")
        print(f"Times: {time1} vs {time2}")
        print(f"Modo: {modo.replace('-', ' ').title()}\n")

        # Seleção de mapas
        try:
            mapas = vetar_e_escolher_mapas(time1, time2)
            if not mapas:
                raise RuntimeError("Nenhum mapa válido selecionado")
        except Exception as e:
            print(f"Erro na seleção de mapas: {str(e)}")
            return None

        # Execução dos mapas
        for mapa in mapas:
            try:
                print(f"\n=== MAPA: {mapa.upper()} ===")
                resultado_mapa = jogar_mapa(time1, time2, mapa, modo, jogadores_time1, jogadores_time2)
                
                if hasattr(resultado_mapa, 'erro'):
                    print(f"Mapa {mapa} ignorado devido a erros")
                    continue
                
                resultado.mapas.append(resultado_mapa)
                
                vitorias_time1 = sum(1 for m in resultado.mapas if m.placar_time1 > m.placar_time2)
                vitorias_time2 = sum(1 for m in resultado.mapas if m.placar_time2 > m.placar_time1)
                
                print(f"\nPlacar atual: {time1} {vitorias_time1}-{vitorias_time2} {time2}")
                
                mostrar_estatisticas_por_mapa(jogadores_time1, jogadores_time2, mapa, time1, time2, times_config)


                if vitorias_time1 >= 2 or vitorias_time2 >= 2:
                    break
                    
            except Exception as e:
                print(f"Erro crítico durante o mapa {mapa}: {str(e)}")
                return resultado  # Retorna resultados parciais
            

        resultado.vencedor, resultado.perdedor = (time1, time2) if vitorias_time1 > vitorias_time2 else (time2, time1)

        print(f"\n=== RESULTADO FINAL ===")
        print(f"VENCEDOR: {resultado.vencedor}")

        print("\n" + "="*40 + "\n🎉 FIM DE JOGO! 🎉")
        print(f"Placar Final: {time1} {vitorias_time1} x {vitorias_time2} {time2}")
        print("="*40 + "\n")
        #print(f"📊 Estatísticas Finais - {time1}:")

        # Mostra os placares dos mapas
        print("\nPlacares dos Mapas:")
        for mapa_result in resultado.mapas:
            print(f"- {mapa_result.mapa}: {time1} {mapa_result.placar_time1} x {mapa_result.placar_time2} {time2}")
        
        print("="*40 + "\n")
        mostrar_estatisticas_finais(jogadores_time1, jogadores_time2, time1, time2, times_config)

        return resultado

    except Exception as e:
        print(f"Erro fatal na partida: {str(e)}")
        return None

# ==================== EXEMPLO DE USO ====================
    # Cadastre times primeiro usando funcoes_prejogo.adicionar_time()
    
    # Modo manual
    # jogar_partida(modo='manual', time1="FURIA", time2="Liquid")
    
    # Modo semi-automático (usuário controla primeiro time)
    # jogar_partida(modo='semi-auto', time1="Jogador", time2="Bot")
    
    # Modo automático
    # jogar_partida(modo='auto', time1="FURIA", time2="Liquid")

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
        over_normalizado = row['over'] / 80.0
        
        jogadores.append({
            "nome": row['nick'],
            "over": over_normalizado,
            "role": row['funcao'],
            "estatisticas": {
                "mapas": {},      # estatísticas individuais por mapa
                "total": {"kills": 0, "deaths": 0, "rounds": 0}
            }
        })
    return jogadores


def calcular_probabilidade_vitoria(over_ct, over_tr, lado_time, estrategia_ct, estrategia_tr, mapa, k=0.1):
    peso_over = 0.3
    peso_lado = 0.3
    peso_estrategia = 0.6
    peso_randomico = 1.2

    diferenca_over = over_ct - over_tr
    vantagem_lado = 1 if lado_time == "ct" else -1
    resultado_estrategia = estrategia_resultado(estrategia_ct, estrategia_tr, mapa)
    vantagem_estrategia = 1 if resultado_estrategia == "ct" else -1

    score = (
        (peso_over * diferenca_over) +
        (peso_lado * vantagem_lado) +
        (peso_estrategia * vantagem_estrategia) +
        (peso_randomico * random.uniform(-1, 1))
    )

    # Função sigmoide para limitar extremos
    probabilidade = 1 / (1 + math.exp(-k * score))
    return probabilidade


def resetar_estatisticas_para_mapa(jogadores: list[dict], mapa: str):
    for j in jogadores:
        # Cria a chave "estatisticas" se não existir, sem tocar nos outros campos
        if "estatisticas" not in j:
            j["estatisticas"] = {}
        if "mapas" not in j["estatisticas"]:
            j["estatisticas"]["mapas"] = {}

        # Apenas reseta kills/deaths e rounds do mapa atual
        j["estatisticas"]["mapas"][mapa] = {"kills": 0, "deaths": 0, "rounds": 0}

def decidir_vencedor_round(
    over_ct: float, 
    over_tr: float, 
    lado_time: str, 
    estrategia_ct: str, 
    estrategia_tr: str,
    mapa :str
) -> str:
    """
    Decide o vencedor do round com base no over, lado, estratégias e fator randômico.
    """
    probabilidade_ct = calcular_probabilidade_vitoria(over_ct, over_tr, lado_time, estrategia_ct, estrategia_tr, mapa)

    if random.random() < probabilidade_ct:
        return "ct"
    else:
        return "tr"
    
# dicionário de times carregados do CSV
def carregar_times_config(caminho_csv="times.csv"):
    config = {}
    with open(caminho_csv, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cor = getattr(Fore, row["cor"].upper(), "")
            config[row["nome"]] = {
                "emoji": row["emoji"],
                "cor": cor
            }
    return config

def mostrar_estatisticas_por_mapa(jogadores_time1, jogadores_time2, mapa, nome_time1, nome_time2, config):
    print(f"\n📊 Estatísticas no mapa {mapa}:")

    for nome_time, jogadores in [(nome_time1, jogadores_time1), (nome_time2, jogadores_time2)]:
        cfg = config.get(nome_time, {"emoji": "", "cor": ""})
        cor, emoji = cfg["cor"], cfg["emoji"]

        print(f"\n➡️ {cor}{emoji} {nome_time}{Style.RESET_ALL}")
        for p in sorted(jogadores, key=lambda x: x["estatisticas"]["mapas"][mapa]["kills"], reverse=True):
            k = p["estatisticas"]["mapas"][mapa]["kills"]
            d = p["estatisticas"]["mapas"][mapa]["deaths"]
            diff = k - d
            print(f" - {p['nome']:<12} | "
                  f"K: {cor}{k:<3}{Style.RESET_ALL} "
                  f"D: {d:<3} | "
                  f"+/-: {diff:<3} | "
                  f"Role: {p['role']}")


def mostrar_estatisticas_finais(jogadores_time1, jogadores_time2, nome_time1, nome_time2, config):
    print("\n📊 Estatísticas finais acumuladas:")

    for nome_time, jogadores in [(nome_time1, jogadores_time1), (nome_time2, jogadores_time2)]:
        cfg = config.get(nome_time, {"emoji": "", "cor": ""})
        cor, emoji = cfg["cor"], cfg["emoji"]

        print(f"\n➡️ {cor}{emoji} {nome_time} (Totais){Style.RESET_ALL}")
        for p in sorted(jogadores, key=lambda x: x["estatisticas"]["total"]["kills"], reverse=True):
            k = p["estatisticas"]["total"]["kills"]
            d = p["estatisticas"]["total"]["deaths"]
            diff = k - d
            print(f" - {p['nome']:<12} | "
                  f"K: {cor}{k:<3}{Style.RESET_ALL} "
                  f"D: {d:<3} | "
                  f"+/-: {diff:<3} | "
                  f"Role: {p['role']}")

    # Resumo por mapa
    print("\n📌 Estatísticas por mapa:")
    mapas = list(jogadores_time1[0]["estatisticas"]["mapas"].keys())

    for mapa in mapas:
        print(f"\nMapa {mapa}:")
        for nome_time, jogadores in [(nome_time1, jogadores_time1), (nome_time2, jogadores_time2)]:
            cfg = config.get(nome_time, {"emoji": "", "cor": ""})
            cor, emoji = cfg["cor"], cfg["emoji"]

            print(f"\n➡️ {cor}{emoji} {nome_time}{Style.RESET_ALL}")
            for p in sorted(jogadores, key=lambda x: x["estatisticas"]["mapas"][mapa]["kills"], reverse=True):
                k = p["estatisticas"]["mapas"][mapa]["kills"]
                d = p["estatisticas"]["mapas"][mapa]["deaths"]
                print(f" - {p['nome']:<12} | "
                      f"K: {cor}{k:<3}{Style.RESET_ALL} "
                      f"D: {d:<3}")


from collections import defaultdict
import pandas as pd

from collections import defaultdict
import pandas as pd

def simular_partidas_em_lote_auto(time1: str, time2: str, n: int = 100, modo: ModoJogo = "auto"):
    """
    Simula N partidas entre dois times, escolhendo mapas automaticamente,
    e retorna K/D acumulado dos jogadores ao longo de todas as partidas.
    """
    resultados_partidas = []
    
    # Estatísticas agregadas globais
    kills_agg = defaultdict(list)
    deaths_agg = defaultdict(list)
    times_jogador = {}  # salvar qual time cada jogador pertence
    vitorias = {time1: 0, time2: 0}

    for i in range(n):
        print(f"\n=== Simulação {i+1}/{n} ===")
        
        # Escolhe mapas aleatoriamente (pode ser 3 mapas por partida)
        mapas_disponiveis = list(estrategias_por_mapa.keys())
        mapas_escolhidos = random.sample(mapas_disponiveis, min(3, len(mapas_disponiveis)))
        
        # Carrega jogadores
        df_jogadores = carregar_jogadores_de_arquivo("jogadores.csv")
        jogadores_time1 = obter_jogadores(time1, df_jogadores)
        jogadores_time2 = obter_jogadores(time2, df_jogadores)
        
        # salvar times
        for j in jogadores_time1:
            times_jogador[j["nome"]] = time1
        for j in jogadores_time2:
            times_jogador[j["nome"]] = time2
        
        resultado = ResultadoPartida(
            partida_id=ContadorPartidas.proxima_partida(),
            mapas=[]
        )
        
        for mapa in mapas_escolhidos:
            resultado_mapa = jogar_mapa(time1, time2, mapa, modo, jogadores_time1, jogadores_time2)
            resultado.mapas.append(resultado_mapa)

            # Agrega kills e deaths globais
            for jogador in jogadores_time1 + jogadores_time2:
                kills_agg[jogador["nome"]].append(jogador["estatisticas"]["mapas"][mapa]["kills"])
                deaths_agg[jogador["nome"]].append(jogador["estatisticas"]["mapas"][mapa]["deaths"])

        # Determina vencedor da partida
        vitorias_time1 = sum(1 for m in resultado.mapas if m.placar_time1 > m.placar_time2)
        vitorias_time2 = sum(1 for m in resultado.mapas if m.placar_time2 > m.placar_time1)
        vencedor = time1 if vitorias_time1 > vitorias_time2 else time2
        vitorias[vencedor] += 1
        
        resultados_partidas.append(resultado)
    
    # Calcula médias globais por jogador
    kd_geral = {}
    for jogador in kills_agg.keys():
        total_kills = sum(kills_agg[jogador])
        total_deaths = sum(deaths_agg[jogador])
        kd_geral[jogador] = {
            "Time": times_jogador[jogador],
            "Kills": round(total_kills / n, 2),
            "Deaths": round(total_deaths / n, 2),
            "K/D": round((total_kills / total_deaths) if total_deaths != 0 else float('inf'), 2)
        }

    # Converte em DataFrame para mostrar tabela organizada
    kd_df = pd.DataFrame(kd_geral).T
    kd_df = kd_df.sort_values(by=["Time", "K/D"], ascending=[True, False])

    # Exibe resumo
    print("\n=== RESUMO DA SIMULAÇÃO ===")
    print(f"Total de partidas simuladas: {n}")
    print(f"Vitórias: {time1}: {vitorias[time1]}, {time2}: {vitorias[time2]}\n")
    
    print("\n📊 Média de K/D acumulado por jogador:")
    print(kd_df)

    return resultados_partidas, vitorias, kd_df

# Mesma função, adaptada para um jogo apenas
def simular_partida_auto(time1: str, time2: str, fase, modo: ModoJogo = "auto"):
    """
    Simula 1 partida entre dois times, escolhendo mapas automaticamente,
    e retorna o vencedor, perdedor e ResultadoPartida completo com estatísticas atualizadas.
    """
    resultado = ResultadoPartida(partida_id=ContadorPartidas.proxima_partida(), mapas=[])
    
    # Carrega jogadores
    df_jogadores = carregar_jogadores_de_arquivo("jogadores.csv")

    jogadores_time1 = [{
    "nome": j["nome"],
    "time": time1,
    "kills": 0,
    "deaths": 0,
    "rounds": 0,
    "over": j.get("over", 1.0),
    "role": j.get("role", "rifler"),
    "estatisticas": {
        "mapas": {},              # estatísticas por mapa
        "total": {"kills": 0, "deaths": 0, "rounds": 0}  # estatísticas gerais
    }
    } for j in obter_jogadores(time1, df_jogadores)]

    jogadores_time2 = [{
        "nome": j["nome"],
        "time": time2,
        "kills": 0,
        "deaths": 0,
        "rounds": 0,
        "over": j.get("over", 1.0),
        "role": j.get("role", "rifler"),
        "estatisticas": {
        "mapas": {},
        "total": {"kills": 0, "deaths": 0, "rounds": 0}
        }
    } for j in obter_jogadores(time2, df_jogadores)]


    # Escolhe os mapas
    mapas_escolhidos = random.sample(list(estrategias_por_mapa.keys()), min(3, len(estrategias_por_mapa)))
    
    vitorias_time1 = 0
    vitorias_time2 = 0

    for mapa in mapas_escolhidos:

        resultado_mapa = jogar_mapa(time1, time2, mapa, modo, jogadores_time1, jogadores_time2)
        resultado_mapa.fase = fase
        resultado.mapas.append(resultado_mapa)
        vitorias_time1 = sum(1 for m in resultado.mapas if m.placar_time1 > m.placar_time2)
        vitorias_time2 = sum(1 for m in resultado.mapas if m.placar_time2 > m.placar_time1)

        # Verifica condição de vitória da partida
        if vitorias_time1 == 2 or vitorias_time2 == 2:
            break

    # Determina o vencedor final com base nas vitórias
    if vitorias_time1 > vitorias_time2:
        vencedor, perdedor = time1, time2
    else:
        vencedor, perdedor = time2, time1  

    # Adiciona estatísticas finais no ResultadoPartida
    #resultado.fase = fase
    resultado.estatisticas_jogadores = jogadores_time1 + jogadores_time2
    
    return vencedor, perdedor, resultado


# Exemplo de uso:
# resultados, vitorias, kills_media, deaths_media = simular_partidas_em_lote("FURIA", "MIBR", n=100)

import random
from collections import defaultdict

def simular_torneio_mata_mata(times, simular_partida_auto):
    """
    Simula um torneio de mata-mata completo.
    Retorna o ranking final, vitórias/derrotas e todas as partidas jogadas.
    """
    vitorias = {time: 0 for time in times}
    derrotas = {time: 0 for time in times}
    partidas_jogadas = []
    rodada = 1

    while len(times) > 1:

        # Define o nome da fase conforme o número de times restantes
        if len(times) == 16:
            fase = "Oitavas de Final"
        elif len(times) == 8:
            fase = "Quartas de Final"
        elif len(times) == 4:
            fase = "Semifinal"
        elif len(times) == 2:
            fase = "Final"
        else:
            fase = f"Rodada {rodada}"

        print(f"\n=== {fase} ===")

        vencedores = []
        random.shuffle(times)

        for i in range(0, len(times), 2):
            time1 = times[i]
            time2 = times[i + 1]

            vencedor, perdedor, resultado = simular_partida_auto(time1, time2, fase)
            partidas_jogadas.append(resultado)

            vitorias[vencedor] += 1
            derrotas[perdedor] += 1
            vencedores.append(vencedor)

        times = vencedores
        rodada += 1

    ranking = list(vitorias.keys())
    ranking.sort(key=lambda t: (-vitorias[t], derrotas[t]))

    return ranking, vitorias, derrotas, partidas_jogadas



def simular_torneios_em_lote(times, simular_partida, n=1):
    """
    Simula múltiplos torneios e coleta estatísticas de desempenho e partidas completas.
    Retorna:
      - estatísticas agregadas por time
      - lista de todas as partidas jogadas (ResultadoPartida)
    """
    estatisticas = {
        time: {
            "campeao": 0,
            "vice": 0,
            "top4": 0,
            "posicoes": [],
            "vitorias_total": 0,
            "derrotas_total": 0
        }
        for time in times
    }

    todas_as_partidas = []

    for i in range(n):
        print(f"\n🏆 Simulando Torneio {i+1}/{n}")
        ranking, vitorias, derrotas, partidas_jogadas = simular_torneio_mata_mata(times[:], simular_partida_auto)
        todas_as_partidas.extend(partidas_jogadas)

        # Atualiza estatísticas dos times
        for pos, time in enumerate(ranking, start=1):
            estatisticas[time]["posicoes"].append(pos)
            estatisticas[time]["vitorias_total"] += vitorias.get(time, 0)
            estatisticas[time]["derrotas_total"] += derrotas.get(time, 0)

            if pos == 1:
                estatisticas[time]["campeao"] += 1
            elif pos == 2:
                estatisticas[time]["vice"] += 1
            elif pos in (3, 4):
                estatisticas[time]["top4"] += 1

    # Calcula médias
    for time in estatisticas:
        posicoes = estatisticas[time]["posicoes"]
        estatisticas[time]["posicao_media"] = sum(posicoes) / len(posicoes)
        estatisticas[time]["vitorias_media"] = estatisticas[time]["vitorias_total"] / n
        estatisticas[time]["vitorias"] = estatisticas[time]["vitorias_total"]
        estatisticas[time]["derrotas"] = estatisticas[time]["derrotas_total"]

    return {
        "estatisticas": estatisticas,
        "partidas": todas_as_partidas,
        "ranking": ranking
        }



# ======== EXEMPLO DE USO ========

# Exemplo de uso:
# simular_torneios_em_lote(times: List[str], n_torneios: int = 50)

