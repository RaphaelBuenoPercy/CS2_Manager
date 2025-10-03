import random
import csv
from typing import List, Dict
import re
from funcoes_simulacao_deepseek import jogar_partida, ResultadoPartida

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

def salvar_resultados_csv(nome_torneio: str, resultados: List[Dict]) -> None:
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
            salvar_resultados_csv(nome_torneio, resultados)

        elif formato == 3:
            campeao, resultados = fase_double_elimination(times_selecionados, resultados)
            print(f"\n🏆 Campeão: {campeao} 🏆")
            salvar_resultados_csv(nome_torneio, resultados)
            print("CRIAR SALVAR RESULTADOS CSV PARA DOUBLE ELIMINATION, TESTAR COM MAIS QUE 4 TIMES E CRIAR FORMATO SUIÇO")

        else:
            classificados = times_selecionados
            campeao, resultados = fase_mata_mata(classificados, resultados)
            print(f"\n🏆 Campeão: {campeao[0]} 🏆")
            salvar_resultados_csv(nome_torneio, resultados)

    except Exception as e:
        print(f"\nErro durante execução: {str(e)}")