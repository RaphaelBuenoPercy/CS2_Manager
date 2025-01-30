import random
import csv
from typing import List, Dict
from funcoes_simulacao_deepseek import jogar_partida

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
            
            return [times[i-1] for i in indices]
        
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
    print("\nGrupos Sorteados:")
    for i, grupo in enumerate(grupos, 1):
        print(f"Grupo {i}: {', '.join(grupo)}")

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
                    vencedor, _, _, resultado = jogar_partida(0, time1, time2)
                    placares[vencedor] += 3
                    resultados.append(resultado)
        
        # Classificação por pontos
        grupo_ordenado = sorted(placares.items(), key=lambda x: -x[1])
        classificados.extend([time for time, _ in grupo_ordenado[:num_classificados]])
    
    return classificados, resultados

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
        for i in range(0, len(times), 2):
            time1, time2 = times[i], times[i+1]
            vencedor, _, _, resultado = jogar_partida(0, time1, time2)
            resultado["fase"] = fase_atual
            resultados.append(resultado)
            novos_times.append(vencedor)
            print(f"{time1} vs {time2} → {vencedor}")
        
        times = novos_times
    
    return times, resultados

def salvar_resultados_csv(nome_torneio: str, resultados: List[Dict]) -> None:
    """Salva os resultados do torneio em arquivo CSV.
    
    Args:
        nome_torneio: Nome do arquivo sem extensão
        resultados: Lista de dicionários com resultados
    """
    try:
        with open(f"{nome_torneio}_resultados.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=[
                "time1", "time2", "placar_time1", "placar_time2", 
                "vencedor", "mapas", "fase"
            ])
            writer.writeheader()
            writer.writerows(resultados)
        print(f"\nResultados salvos em {nome_torneio}_resultados.csv")
    except Exception as e:
        print(f"Erro ao salvar resultados: {str(e)}")

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
            "Formato (1-Grupos / 2-Mata-mata): ",
            min_val=1,
            max_val=2
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
        else:
            classificados = times_selecionados

        campeao, resultados = fase_mata_mata(classificados, resultados)
        print(f"\n🏆 Campeão: {campeao[0]} 🏆")
        salvar_resultados_csv(nome_torneio, resultados)

    except Exception as e:
        print(f"\nErro durante execução: {str(e)}")