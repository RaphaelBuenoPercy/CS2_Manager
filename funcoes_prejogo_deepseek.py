# funcoes_prejogo_deepseek.py
import csv
import logging
from typing import List, Dict, Optional
from collections import defaultdict
from estrategias_deepseek import estrategias_por_mapa
from config import TIMES_CSV, JOGADORES_CSV

logger = logging.getLogger(__name__)

# Lista compartilhada dos times cadastrados na sessão atual. As funções
# abaixo não dependem mais dela internamente (recebem `lista_times` como
# parâmetro explícito, o que as deixa testáveis com qualquer lista) — mas
# Menu_Helper.py, modo_carreira.py e funcoes_simulacao_deepseek.py ainda
# importam este `times` como a lista canônica da aplicação e a repassam
# adiante para essas funções.
times: List[str] = []


def adicionar_time(nome: str, lista_times: List[str]) -> None:
    """Adiciona um novo time à base de dados, validando entradas.

    Args:
        nome: Nome do time a ser cadastrado

    Raises:
        ValueError: Se nome for vazio ou duplicado
    """
    nome = nome.strip().lower()
    if not nome:
        raise ValueError("Nome do time não pode ser vazio")

    if any(t.lower() == nome.lower() for t in lista_times):
        raise ValueError(f"Time '{nome}' já está registrado")

    lista_times.append(nome)
    print(f"✓ Time '{nome}' adicionado com sucesso\n")


def carregar_times_csv(lista_times: List[str], arquivo: str = TIMES_CSV) -> None:
    """Carrega times de um arquivo CSV validando o formato.

    Args:
        lista_times: Lista para adicionar os times carregados
        arquivo: Caminho do arquivo CSV

    Raises:
        FileNotFoundError: Se o arquivo não existir
    """
    try:
        novos_times = []
        with open(arquivo, "r", newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            for linha in reader:
                if linha and linha[0].strip():
                    nome = linha[0].strip().lower()
                    if nome not in lista_times and nome not in novos_times:
                        novos_times.append(nome)

        lista_times.extend(novos_times)
        print(f"✓ {len(novos_times)} times carregados de '{arquivo}'\n")

    except FileNotFoundError:
        raise FileNotFoundError(f"Arquivo '{arquivo}' não encontrado")
    except Exception as e:
        logger.error("Erro ao ler CSV '%s': %s", arquivo, e)
        print(f"Erro ao ler CSV: {str(e)}\n")


def salvar_times_csv(lista_times: List[str], arquivo: str = TIMES_CSV) -> None:
    """Persiste a lista atual de `times` de volta no CSV.

    Antes, adicionar/remover times pelo menu só alterava a lista em memória:
    ao reiniciar o programa e recarregar o CSV, as mudanças eram perdidas.
    Preserva emoji/cor dos times já cadastrados (usados pela configuração
    visual em carregar_times_config) e grava campos vazios para times novos.
    """
    config_existente: Dict[str, List[str]] = {}
    try:
        with open(arquivo, "r", newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            for linha in reader:
                if linha and linha[0].strip():
                    nome = linha[0].strip().lower()
                    resto = (linha[1:] + ["", ""])[:2]
                    config_existente[nome] = resto
    except FileNotFoundError:
        pass

    try:
        with open(arquivo, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            for nome in lista_times:
                emoji, cor = config_existente.get(nome, ["", ""])
                writer.writerow([nome, emoji, cor])
        logger.info("Times persistidos em '%s' (%d times)", arquivo, len(lista_times))
    except Exception as e:
        logger.error("Erro ao salvar '%s': %s", arquivo, e)
        print(f"⚠️ Não foi possível salvar as alterações em '{arquivo}': {e}")


def calcular_over_medio(time_nome: str, arquivo_csv: str = JOGADORES_CSV) -> float:
    """
    Calcula o over médio de um time com base no arquivo CSV de jogadores.

    Args:
        time_nome: Nome do time.
        arquivo_csv: Caminho do arquivo CSV com os dados dos jogadores.

    Returns:
        Over médio do time.
    """
    try:
        with open(arquivo_csv, "r", newline="", encoding="utf-8") as csvfile:
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


def listar_times(lista_times: List[str]) -> None:
    """Exibe todos os times registrados formatados."""

    try:
        if not lista_times:
            print("Nenhum time registrado\n")
            return

        print("\nTimes registrados:")
        for i, time in enumerate(lista_times, 1):
            print(f"  {i}. {time}")
        print(f"Total: {len(lista_times)} times\n")

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

        print("\n" + "=" * 40)
        print(" SISTEMA DE VETO DE MAPAS ".center(40, "="))
        print("=" * 40)

        # Fase 1 - Primeiros vetos
        print("\nFASE 1 - PRIMEIROS VETOS")
        print("-" * 40)
        print(f"{time1}, banir primeiro mapa:")
        veto1 = selecionar_mapa(time1, mapas_disponiveis)

        print(f"{time2}, banir primeiro mapa:")
        veto2 = selecionar_mapa(time2, mapas_disponiveis)

        # Fase 2 - Escolhas
        print("\nFASE 2 - ESCOLHA DE MAPAS")
        print("-" * 40)
        print(f"{time1}, escolher mapa:")
        pick1 = selecionar_mapa(time1, mapas_disponiveis)

        print(f"{time2}, escolher mapa:")
        pick2 = selecionar_mapa(time2, mapas_disponiveis)

        # Fase 3 - Vetos finais
        print("\nFASE 3 - VETOS FINAIS")
        print("-" * 40)
        print(f"{time1}, banir segundo mapa:")
        veto3 = selecionar_mapa(time1, mapas_disponiveis)

        print(f"{time2}, banir segundo mapa:")
        veto4 = selecionar_mapa(time2, mapas_disponiveis)

        # Mapa decisivo automático
        mapa_decisivo = mapas_disponiveis[0]
        print("\n" + "=" * 40)
        print(f" MAPA DECISIVO: {mapa_decisivo} ".center(40, "•"))
        print("=" * 40 + "\n")

        return [pick1, pick2, mapa_decisivo]

    except Exception as e:
        print(f"Erro no sistema de veto: {str(e)}")
        return []


def calcular_overs_medios_times(arquivo_csv: str = JOGADORES_CSV) -> dict:
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
        with open(arquivo_csv, "r", newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for linha in reader:
                time_nome = linha["time"].strip().lower()
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
