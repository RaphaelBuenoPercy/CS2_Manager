import random
from dataclasses import dataclass
from typing import List, Tuple, Dict, Literal
from estrategias_deepseek import estrategias_por_mapa, estrategia_resultado
from funcoes_prejogo_deepseek import times, vetar_e_escolher_mapas, calcular_over_medio

# ==================== CLASSES DE DADOS ====================
@dataclass
class ResultadoMapa:
    mapa: str
    time_ct: str
    time_tr: str
    placar_time1: int
    placar_time2: int
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
    if modo == 'auto':
        return random.randint(0, len(estrategias)-1)
    
    if modo == 'semi-auto' and "Jogador" not in time:
        return random.randint(0, len(estrategias)-1)
    
    print(f"\n{time}, estratégias disponíveis:")
    for i, estrategia in enumerate(estrategias, 1):
        print(f"{i}. {estrategia}")
    
    while True:
        try:
            escolha = int(input("Escolha (número): ")) - 1
            if 0 <= escolha < len(estrategias):
                return escolha
            print("Número inválido!")
        except ValueError:
            print("Digite apenas números!")

# ==================== FUNÇÕES PRINCIPAIS ====================
def jogar_half(
    time_ct: str, 
    time_tr: str, 
    mapa: str,
    modo: ModoJogo,
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
            
            resultado = decidir_vencedor_round(over_ct, over_tr, "ct", idx_ct, idx_tr)

            if resultado == "ct":
                pontos_ct += 1
                print(f"{time_ct} (CT) venceu! CT {pontos_iniciais_ct + pontos_ct}-{pontos_iniciais_tr + pontos_tr} TR")
            else:
                pontos_tr += 1
                print(f"{time_tr} (TR) venceu! CT {pontos_iniciais_ct + pontos_ct}-{pontos_iniciais_tr + pontos_tr} TR")
                
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

def jogar_mapa(time1: str, time2: str, mapa: str, modo: ModoJogo) -> ResultadoMapa:
    """Executa uma partida completa em um mapa"""
    try:
        resultado = ResultadoMapa(mapa=mapa, time_ct=time1, time_tr=time2, placar_time1=0, placar_time2=0)
        
        # Primeiro half (CT: time1, TR: time2)
        resultado.placar_time1, resultado.placar_time2 = jogar_half(
            time1, time2, mapa, modo, 12, meta=13
        )

        # Segundo half (CT: time2, TR: time1) com pontos iniciais
        if resultado.placar_time1 < 13 and resultado.placar_time2 < 13:
            placar_time2_half, placar_time1_half = jogar_half(
                time2,  # CT
                time1,  # TR
                mapa,
                modo,
                max_rounds=12,
                meta=13,
                pontos_iniciais_ct=resultado.placar_time2,  # Pontos atuais do time2 (CT)
                pontos_iniciais_tr=resultado.placar_time1   # Pontos atuais do time1 (TR)
            )
            resultado.placar_time1 += placar_time1_half
            resultado.placar_time2 += placar_time2_half

        # Verificar empate e iniciar overtime
        if resultado.placar_time1 == resultado.placar_time2:
            overtime_count = 1
            resultado = jogar_ot(time1, time2, mapa, modo, resultado, overtime_count)

        return resultado

    except Exception as e:
        print(f"Erro durante a execução do mapa {mapa}: {str(e)}")
        resultado.erro = True
        return resultado

def jogar_ot(time1: str, time2: str, mapa: str, modo: ModoJogo, resultado, overtime_count) -> ResultadoMapa:
        while True:
            print(f"\n=== Overtime {overtime_count} (Placar: {resultado.placar_time1}-{resultado.placar_time2}) ===")
            
            # Jogar até 4 vitórias no overtime, alternando lados a cada 3 rounds
            placar_meta = 13 + (overtime_count * 3)  # Meta para vencer o overtime
        
            # Primeiro lado do overtime (Time 1 CT)  
            # Jogar rounds alternados até atingir 4 vitórias
            while True:
                # Primeiro Half Overtime
                placar_time1_1ot, placar_time2_1ot = jogar_half(
                    time1, #CT
                    time2, #TR 
                    mapa, 
                    modo, 
                    max_rounds=3, 
                    meta=placar_meta,
                    pontos_iniciais_ct=resultado.placar_time1,
                    pontos_iniciais_tr=resultado.placar_time2
                 )
                
                resultado.placar_time1 += placar_time1_1ot
                resultado.placar_time2 += placar_time2_1ot
                
                # TR joga até 3 rounds OU até atingir 4 vitórias
                placar_time2_1ot, placar_time1_1ot = jogar_half(
                    time2, #CT
                    time1, #TR 
                    mapa, 
                    modo, 
                    max_rounds=3, 
                    meta=placar_meta,
                    pontos_iniciais_ct=resultado.placar_time2,
                    pontos_iniciais_tr=resultado.placar_time1
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
                return jogar_ot(time1, time2, mapa, modo, resultado, overtime_count)

def jogar_partida(
    modo: ModoJogo = 'manual',
    time1: str = None,
    time2: str = None,
    fase_torneio: str = None ) -> ResultadoPartida:
    """Gerencia uma partida completa entre dois times"""
    try:
        # Validação inicial
        try:
            time1 = validar_time(time1) if time1 else random.choice(times)
            time2 = validar_time(time2) if time2 else random.choice([t for t in times if t != time1])
        except (ValueError, IndexError) as e:
            raise RuntimeError(f"Seleção de times inválida: {str(e)}") from e

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
                resultado_mapa = jogar_mapa(time1, time2, mapa, modo)
                
                if hasattr(resultado_mapa, 'erro'):
                    print(f"Mapa {mapa} ignorado devido a erros")
                    continue
                
                resultado.mapas.append(resultado_mapa)
                
                vitorias_time1 = sum(1 for m in resultado.mapas if m.placar_time1 > m.placar_time2)
                vitorias_time2 = sum(1 for m in resultado.mapas if m.placar_time2 > m.placar_time1)
                
                print(f"\nPlacar atual: {time1} {vitorias_time1}-{vitorias_time2} {time2}")
                
                if vitorias_time1 >= 2 or vitorias_time2 >= 2:
                    break

            except Exception as e:
                print(f"Erro crítico durante o mapa {mapa}: {str(e)}")
                return resultado  # Retorna resultados parciais

        resultado.vencedor, resultado.perdedor = (time1, time2) if vitorias_time1 > vitorias_time2 else (time2, time1)
        print(f"\n=== RESULTADO FINAL ===")
        print(f"VENCEDOR: {resultado.vencedor}")

        # Mostra os placares dos mapas
        print("\nPlacares dos Mapas:")
        for mapa_result in resultado.mapas:
            print(f"- {mapa_result.mapa}: {time1} {mapa_result.placar_time1} x {mapa_result.placar_time2} {time2}")
        
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


def calcular_probabilidade_vitoria(
    over_ct: float, 
    over_tr: float, 
    lado_time: str, 
    estrategia_ct: str, 
    estrategia_tr: str, 
    fator_randomico: float = 0.1
) -> float:
    """
    Calcula a probabilidade de vitória do time CT com base no over, lado, estratégias e fator randômico.
    """
    # Peso do over dos times
    peso_over = 0.4
    # Peso do lado do time (CT ou TR)
    peso_lado = 0.3
    # Peso das estratégias
    peso_estrategia = 0.2
    # Peso do fator randômico
    peso_randomico = 0.1

    # Diferença de over entre os times
    diferenca_over = over_ct - over_tr

    # Vantagem do lado (CT ou TR)
    vantagem_lado = 1 if lado_time == "ct" else -1

    # Resultado das estratégias
    resultado_estrategia = estrategia_resultado(estrategia_ct, estrategia_tr)
    vantagem_estrategia = 1 if resultado_estrategia == "ct" else -1

    # Cálculo da probabilidade
    probabilidade = (
        (peso_over * diferenca_over) +
        (peso_lado * vantagem_lado) +
        (peso_estrategia * vantagem_estrategia) +
        (peso_randomico * random.uniform(-1, 1))
    )

    # Normaliza a probabilidade para um valor entre 0 e 1
    probabilidade = (probabilidade + 1) / 2
    return probabilidade

def decidir_vencedor_round(
    over_ct: float, 
    over_tr: float, 
    lado_time: str, 
    estrategia_ct: str, 
    estrategia_tr: str
) -> str:
    """
    Decide o vencedor do round com base no over, lado, estratégias e fator randômico.
    """
    probabilidade_ct = calcular_probabilidade_vitoria(over_ct, over_tr, lado_time, estrategia_ct, estrategia_tr)
    if random.random() < probabilidade_ct:
        return "ct"
    else:
        return "tr"