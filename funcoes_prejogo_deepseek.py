# funcoes_prejogo_deepseek.py
import csv
from typing import List, Dict

from typing import List, Dict, Optional

import csv
from typing import List, Dict, Optional

class Jogador:
    def __init__(self, nick: str, nacionalidade: str, funcao: str, over: float = 0.0):
        self.nick = nick
        self.nacionalidade = nacionalidade
        self.funcao = funcao
        self.over = over
        self.estatisticas: Dict[str, Dict[str, int]] = {}  # Ex: {"torneio1": {"kills": 10, "mortes": 5, "first_kills": 2}}
        self.time: Optional[Time] = None  # Referência ao time ao qual o jogador pertence

    def adicionar_estatistica(self, torneio: str, kills: int, mortes: int, first_kills: int) -> None:
        """Adiciona estatísticas para o jogador em um torneio específico."""
        self.estatisticas[torneio] = {
            "kills": kills,
            "mortes": mortes,
            "first_kills": first_kills
        }

    def get_time(self) -> Optional[str]:
        """Retorna o nome do time ao qual o jogador pertence, ou None se não estiver em um time."""
        return self.time.nome if self.time else None

    def __str__(self) -> str:
        time_nome = self.get_time() or "Sem time"
        return f"Jogador(nick={self.nick}, nacionalidade={self.nacionalidade}, funcao={self.funcao}, over={self.over}, time={time_nome})"

class Time:
    def __init__(self, nome: str):
        self.nome = nome
        self.jogadores: List[Jogador] = []

    def adicionar_jogador(self, jogador: Jogador) -> None:
        """Adiciona um jogador ao time e atualiza a referência do time no jogador."""
        if jogador.time:
            raise ValueError(f"Jogador {jogador.nick} já pertence ao time {jogador.time.nome}")
        self.jogadores.append(jogador)
        jogador.time = self
        print(f"✓ Jogador {jogador.nick} adicionado ao time {self.nome}")

    def remover_jogador(self, nick: str) -> Optional[Jogador]:
        """Remove um jogador do time pelo nick e remove a referência do time no jogador."""
        for jogador in self.jogadores:
            if jogador.nick == nick:
                self.jogadores.remove(jogador)
                jogador.time = None
                print(f"✗ Jogador {nick} removido do time {self.nome}")
                return jogador
        return None

    def listar_jogadores(self) -> None:
        """Lista todos os jogadores do time."""
        print(f"Jogadores do time {self.nome}:")
        for jogador in self.jogadores:
            print(jogador)

    def carregar_jogadores_csv(self, arquivo: str) -> None:
        """Carrega jogadores de um arquivo CSV e os adiciona ao time."""
        try:
            with open(arquivo, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for linha in reader:
                    try:
                        # Informações básicas
                        nick = linha["nick"]
                        nacionalidade = linha["nacionalidade"]
                        funcao = linha["funcao"]
                        over = float(linha.get("over", 0.0))  # Valor padrão 0.0 se "over" não estiver no CSV

                        # Cria o jogador
                        jogador = Jogador(nick=nick, nacionalidade=nacionalidade, funcao=funcao, over=over)

                        # Processa as estatísticas em torneios
                        for coluna, valor in linha.items():
                            if "_kills" in coluna or "_mortes" in coluna or "_first_kills" in coluna:
                                torneio, estatistica = coluna.split("_")
                                if torneio not in jogador.estatisticas:
                                    jogador.estatisticas[torneio] = {}
                                jogador.estatisticas[torneio][estatistica] = int(valor)

                        # Adiciona o jogador ao time
                        time_nome = linha.get("time")
                        if time_nome and time_nome.strip().lower() == self.nome.lower():
                            self.adicionar_jogador(jogador)
                    except KeyError as e:
                        print(f"Erro ao processar linha: {linha}. Campo obrigatório faltando: {e}")
                    except ValueError as e:
                        print(f"Erro ao processar linha: {linha}. Valor inválido: {e}")
        except FileNotFoundError:
            print(f"Erro: Arquivo '{arquivo}' não encontrado.")
        except Exception as e:
            print(f"Erro ao ler o arquivo CSV: {e}")

    def __str__(self) -> str:
        return f"Time(nome={self.nome}, total_jogadores={len(self.jogadores)})"

# Exemplo de uso
if __name__ == "__main__":
    # Criando times
    time_a = Time("Time A")
    time_b = Time("Time B")

    # Carregando jogadores de um arquivo CSV
    time_a.carregar_jogadores_csv("jogadores.csv")
    time_b.carregar_jogadores_csv("jogadores.csv")

    # Listando jogadores dos times
    time_a.listar_jogadores()
    time_b.listar_jogadores()


# Base de dados dos times
times: List[str] = []

# Estratégias importadas
from estrategias_deepseek import estrategias_por_mapa

def adicionar_time(nome: str) -> None:
    """Adiciona um novo time à base de dados, validando entradas.
    
    Args:
        nome: Nome do time a ser cadastrado
        
    Raises:
        ValueError: Se nome for vazio ou duplicado
    """
    global times
    nome = nome.strip()
    if not nome:
        raise ValueError("Nome do time não pode ser vazio")
            
    if nome in times:
        raise ValueError(f"Time '{nome}' já está registrado")
            
    times.append(nome)
    print(f"✓ Time '{nome}' adicionado com sucesso\n")

def carregar_times_csv(arquivo: str = "times.csv") -> None:
    """Carrega times de um arquivo CSV validando o formato.
    
    Args:
        arquivo: Caminho do arquivo CSV
        
    Raises:
        FileNotFoundError: Se o arquivo não existir
    """
    global times
    try:
        novos_times = []
        with open(arquivo, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for linha in reader:
                if linha and linha[0].strip():
                    nome = linha[0].strip()
                    if nome not in times and nome not in novos_times:
                        novos_times.append(nome)
        
        times.extend(novos_times)
        print(f"✓ {len(novos_times)} times carregados de '{arquivo}'\n")
        
    except FileNotFoundError:
        raise FileNotFoundError(f"Arquivo '{arquivo}' não encontrado")
    except Exception as e:
        print(f"Erro ao ler CSV: {str(e)}\n")

def calcular_over_medio(time_nome: str, arquivo_csv: str = "jogadores.csv") -> float:
    """
    Calcula o over médio de um time com base no arquivo CSV de jogadores.
    
    Args:
        time_nome: Nome do time.
        arquivo_csv: Caminho do arquivo CSV com os dados dos jogadores.
    
    Returns:
        Over médio do time.
    """
    try:
        with open(arquivo_csv, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            overs = []
            for linha in reader:
                if linha["time"].strip().lower() == time_nome.strip().lower():
                    overs.append(float(linha["over"]))
                    overs.sort()
            if not overs:
                raise ValueError(f"Nenhum jogador encontrado para o time '{time_nome}'")
            return sum(overs) / len(overs)
    except FileNotFoundError:
        raise FileNotFoundError(f"Arquivo '{arquivo_csv}' não encontrado")
    except Exception as e:
        raise RuntimeError(f"Erro ao calcular over médio: {str(e)}")

def listar_times() -> None:
    """Exibe todos os times registrados formatados."""
    global times
    try:
        if not times:
            print("Nenhum time registrado\n")
            return
            
        print("\nTimes registrados:")
        for i, time in enumerate(times, 1):
            print(f"  {i}. {time}")
        print(f"Total: {len(times)} times\n")
        
    except Exception as e:
        print(f"Erro ao listar times: {str(e)}\n")

def selecionar_mapa(time: str, mapas_disponiveis: List[str]) -> str:
    """Interface para seleção de mapas via números.
    
    Args:
        time: Nome do time fazendo a seleção
        mapas_disponiveis: Lista atual de mapas
        
    Returns:
        Mapa selecionado (removido da lista)
    """
    print(f"\n{time}:")
    print("Mapas disponíveis:")
    for i, mapa in enumerate(mapas_disponiveis, 1):
        print(f"  {i}. {mapa}")
        
    while True:
        try:
            escolha = int(input("Digite o número do mapa: ")) - 1
            if 0 <= escolha < len(mapas_disponiveis):
                mapa_selecionado = mapas_disponiveis.pop(escolha)
                print(f"↳ {mapa_selecionado} selecionado\n")
                return mapa_selecionado
            print("Número inválido!")
        except ValueError:
            print("Digite apenas números!")

def vetar_e_escolher_mapas(time1: str, time2: str) -> List[str]:
    """Gerencia todo o processo de veto e escolha de mapas.
    
    Args:
        time1: Nome do primeiro time
        time2: Nome do segundo time
        
    Returns:
        Lista com 3 mapas selecionados [pick1, pick2, decider]
    """
    try:
        # Cria cópia para não alterar o original
        mapas_disponiveis = list(estrategias_por_mapa.keys()).copy()
        
        if len(mapas_disponiveis) < 7:
            raise ValueError("Mínimo de 7 mapas necessário para veto")
            
        print("\n" + "="*40)
        print(" SISTEMA DE VETO DE MAPAS ".center(40, "="))
        print("="*40)
        
        # Fase 1 - Primeiros vetos
        print("\nFASE 1 - PRIMEIROS VETOS")
        print("-"*40)
        print(f"{time1}, banir primeiro mapa:")
        veto1 = selecionar_mapa(time1, mapas_disponiveis)
        
        print(f"{time2}, banir primeiro mapa:")
        veto2 = selecionar_mapa(time2, mapas_disponiveis)
        
        # Fase 2 - Escolhas
        print("\nFASE 2 - ESCOLHA DE MAPAS")
        print("-"*40)
        print(f"{time1}, escolher mapa:")
        pick1 = selecionar_mapa(time1, mapas_disponiveis)
        
        print(f"{time2}, escolher mapa:")
        pick2 = selecionar_mapa(time2, mapas_disponiveis)
        
        # Fase 3 - Vetos finais
        print("\nFASE 3 - VETOS FINAIS")
        print("-"*40)
        print(f"{time1}, banir segundo mapa:")
        veto3 = selecionar_mapa(time1, mapas_disponiveis)
        
        print(f"{time2}, banir segundo mapa:")
        veto4 = selecionar_mapa(time2, mapas_disponiveis)
        
        # Mapa decisivo automático
        mapa_decisivo = mapas_disponiveis[0]
        print("\n" + "="*40)
        print(f" MAPA DECISIVO: {mapa_decisivo} ".center(40, "•"))
        print("="*40 + "\n")
        
        return [pick1, pick2, mapa_decisivo]
        
    except Exception as e:
        print(f"Erro no sistema de veto: {str(e)}")
        return []
    
import csv
from collections import defaultdict

def calcular_overs_medios_times(arquivo_csv: str = "jogadores.csv") -> dict:
    """
    Calcula o over médio de todos os times com base no arquivo CSV de jogadores.

    Args:
        arquivo_csv: Caminho do arquivo CSV com os dados dos jogadores.

    Returns:
        Um dicionário onde as chaves são os nomes dos times e os valores são os overs médios.
    """
    try:
        # Dicionário para armazenar a soma dos overs e a quantidade de jogadores por time
        times_overs = defaultdict(lambda: {"soma_over": 0.0, "quantidade_jogadores": 0})

        # Ler o arquivo CSV
        with open(arquivo_csv, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for linha in reader:
                time_nome = linha["time"].strip()
                over = float(linha["over"])
                # Atualiza a soma dos overs e a quantidade de jogadores do time
                times_overs[time_nome]["soma_over"] += over
                times_overs[time_nome]["quantidade_jogadores"] += 1

        # Calcular o over médio de cada time
        overs_medios = {}
        for time, dados in times_overs.items():
            if dados["quantidade_jogadores"] > 0:
                overs_medios[time] = dados["soma_over"] / dados["quantidade_jogadores"]
            else:
                overs_medios[time] = 0.0

        return overs_medios

    except FileNotFoundError:
        raise FileNotFoundError(f"Arquivo '{arquivo_csv}' não encontrado")
    except Exception as e:
        raise RuntimeError(f"Erro ao calcular overs médios: {str(e)}")

def exibir_overs_medios_times():
    """
    Exibe os overs médios de todos os times.
    """
    try:
        overs_medios = calcular_overs_medios_times()
        overs_ordenados = sorted(overs_medios.items(), key=lambda x: x[1], reverse=True)
        print("\n=== OVERS MÉDIOS DOS TIMES ===")
        for time, over_medio in overs_ordenados:
            print(f"{time}: {over_medio}")
        print("=" * 30)
    except Exception as e:
        print(f"Erro ao exibir overs médios: {str(e)}")