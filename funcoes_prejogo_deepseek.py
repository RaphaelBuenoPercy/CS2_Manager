# funcoes_prejogo_deepseek.py
import csv
from typing import List, Dict

# Base de dados dos times
times: List[str] = []

# Estratégias importadas
from estrategias import estrategias_por_mapa

def adicionar_time(nome: str) -> None:
    """Adiciona um novo time à base de dados, validando entradas.
    
    Args:
        nome: Nome do time a ser cadastrado
        
    Raises:
        ValueError: Se nome for vazio ou duplicado
    """
    global times
    try:
        nome = nome.strip()
        if not nome:
            raise ValueError("Nome do time não pode ser vazio")
            
        if nome in times:
            raise ValueError(f"Time '{nome}' já está registrado")
            
        times.append(nome)
        print(f"✓ Time '{nome}' adicionado com sucesso\n")
        
    except ValueError as e:
        print(f"Erro: {str(e)}\n")

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