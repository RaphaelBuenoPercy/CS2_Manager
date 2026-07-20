import json
import logging
import random
from funcoes_torneio_deepseek import (
    criar_torneio,
    mostrar_resumo_torneio,
    salvar_estatisticas_torneio,
    mostrar_historico_partidas,
    visualizar_bracket_torneio,
    listar_torneios_salvos,
)
from funcoes_prejogo_deepseek import (
    times,
    listar_times,
    carregar_times_csv,
    salvar_times_csv,
    adicionar_time,
    calcular_overs_medios_times,
    exibir_overs_medios_times,
)
from funcoes_simulacao_deepseek import (
    jogar_partida,
    simular_partidas_em_lote_auto,
    simular_torneios_em_lote,
    simular_partida_auto,
)

# Única implementação de carregar_jogadores_de_arquivo (antes havia uma
# cópia idêntica aqui, outra em funcoes_simulacao_deepseek.py e outra em
# gerador_kills_deaths.py — todas fazendo exatamente a mesma coisa).
from gerador_kills_deaths import carregar_jogadores_de_arquivo
from modo_carreira import menu_carreira

logger = logging.getLogger(__name__)


# ==================== FUNÇÕES AUXILIARES ====================
def mostrar_titulo(texto: str):
    """Exibe títulos formatados"""
    print("\n" + "=" * 50)
    print(f" {texto.upper()} ".center(50, "•"))
    print("=" * 50 + "\n")


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


def confirmar_acao(mensagem: str) -> bool:
    """Solicita confirmação para ações críticas"""
    resposta = input(f"{mensagem} (s/n): ").strip().lower()
    return resposta in ["s", "sim"]


# ==================== SUBMENUS ====================
def menu_gerenciar_times():
    """Submenu para gestão de times"""

    while True:

        mostrar_titulo("gestão de times")
        print("1. Adicionar time")
        print("2. Remover time")
        print("3. Listar times")
        print("4. Calcular Overs dos Times")
        print("5. Testar Partidas em Lotes")
        print("6. Voltar ao menu principal")

        escolha = obter_opcao_numerica(1, 6)

        if escolha == 1:
            nome = input("Nome do novo time: ").strip().lower()
            try:
                adicionar_time(nome)
                salvar_times_csv()
            except ValueError as e:
                # Antes isso não era tratado aqui: um nome vazio ou duplicado
                # derrubava o menu inteiro com uma exceção não capturada.
                print(f"Erro: {e}\n")

        elif escolha == 2:
            listar_times()
            if times:
                try:
                    idx = int(input("Número do time a remover: ")) - 1
                    if 0 <= idx < len(times):
                        if confirmar_acao("Tem certeza que deseja remover este time?"):
                            removed = times.pop(idx)
                            salvar_times_csv()
                            print(f"Time {removed} removido!")
                            print(
                                "Obs.: os jogadores desse time em 'jogadores.csv' "
                                "não foram apagados — edite o arquivo manualmente "
                                "se quiser removê-los também.\n"
                            )
                except ValueError:
                    print("Número inválido!")

        elif escolha == 3:
            listar_times()

        elif escolha == 4:
            calcular_overs_medios_times()
            exibir_overs_medios_times()

        elif escolha == 5:
            time1 = input("Escolha o primeiro time: ")
            time2 = input("Escolha o segundo time: ")
            try:
                qtd = int(input("Escolha o número de vezes que você quer simular: "))
            except ValueError:
                print("Número inválido!")
                continue
            simular_partidas_em_lote_auto(time1, time2, qtd)

        elif escolha == 6:
            return


def menu_partida():
    """Submenu de modos de partida"""
    while True:
        mostrar_titulo("modos de partida")
        print("1. Partida Rápida (Aleatória)")
        print("2. Partida Personalizada")
        print("3. Voltar ao menu principal")

        escolha = obter_opcao_numerica(1, 3)

        if escolha == 1:
            if len(times) >= 2:
                time1, time2 = random.sample(times, 2)
                jogar_partida(modo="auto", time1=time1, time2=time2)
            else:
                print("Necessário pelo menos 2 times registrados!")
        elif escolha == 2:
            if len(times) >= 2:
                listar_times()
                time1 = input("Nome do primeiro time: ").strip().lower()
                time2 = input("Nome do segundo time: ").strip().lower()
                if time1 in times and time2 in times:
                    jogar_partida(modo="manual", time1=time1, time2=time2)
                else:
                    print("Times inválidos!")
            else:
                print("Necessário pelo menos 2 times registrados!")
        elif escolha == 3:
            return


def menu_torneio():
    """Submenu de torneios"""
    while True:
        mostrar_titulo("torneios")
        print("1. Criar novo torneio")
        print("2. Listar torneios anteriores")
        print("3. Simular torneios")
        print("4. Voltar ao menu principal")

        escolha = obter_opcao_numerica(1, 4)

        if escolha == 1:
            criar_torneio(times)
        elif escolha == 2:
            listar_torneios_salvos()
        elif escolha == 3:
            menu_simular_torneio()
            return
        elif escolha == 4:
            return


def menu_simular_torneio():
    if len(times) < 4:
        print("Necessário pelo menos 4 times registrados!")
        return

    listar_times()
    print("\n=== SIMULAÇÃO DE TORNEIO MATA-MATA ===")
    print("Escolha 4 ou 8 times para o torneio.")

    while True:
        try:
            qtd = int(input("Quantos times deseja incluir (4, 8, 16)? ").strip())
            if qtd > len(times):
                print("Não existem times suficientes.")
                return
            elif qtd in (4, 8, 16):
                break
            else:
                print("Digite apenas 4, 8 ou 16.")
        except ValueError:
            print("Entrada inválida, tente novamente.")

    print("\nDigite o nome exato dos times que participarão:")
    times_escolhidos = []
    for i in range(qtd):
        while True:
            nome = input(f"Time {i+1}: ").strip().lower()
            if nome in times and nome not in times_escolhidos:
                times_escolhidos.append(nome)
                break
            elif nome in times_escolhidos:
                print("Esse time já foi escolhido!")
            else:
                print("Time não encontrado. Tente novamente.")

    print(f"\nTimes escolhidos: {', '.join(times_escolhidos)}")

    n = int(input("Quantos torneios você quer simular? "))
    nome_torneio = input("Qual o nome do torneio?: ")

    print(f"\nSimulando {n} torneios automáticos...\n")

    resultados = simular_torneios_em_lote(times_escolhidos, simular_partida_auto, n)

    visualizar_bracket_torneio(resultados["partidas"])

    df, df_total = salvar_estatisticas_torneio(
        resultados["partidas"], resultados["ranking"], nome_torneio
    )

    mostrar_historico_partidas(resultados["partidas"])
    mostrar_resumo_torneio(df, df_total)

    print("\n=== ESTATÍSTICAS GERAIS APÓS", n, "TORNEIOS ===")
    print(
        f"{'Time':<12} | {'Campeão':<8} | {'Vice':<8} | {'Top4':<8} | {'Posição Média':<15} | {'Vitórias Médias':<16} | {'Vitórias':<10} | {'Derrotas':<10}"
    )
    print("-" * 110)

    for time, dados in sorted(
        resultados["estatisticas"].items(), key=lambda x: x[1]["posicao_media"]
    ):

        print(
            f"{time:<12} | "
            f"{dados['campeao']:<8} | "
            f"{dados['vice']:<8} | "
            f"{dados['top4']:<8} | "
            f"{dados['posicao_media']:<15.2f} | "
            f"{dados['vitorias_media']:<16.2f} | "
            f"{dados['vitorias_total']:<10} | "
            f"{dados['derrotas_total']:<10}"
        )


# ==================== MENU PRINCIPAL ====================
def configurar_logging():
    """Configura logging básico: erros/diagnósticos vão para simulador.log,
    sem poluir o console — que continua mostrando só a narrativa do jogo."""
    logging.basicConfig(
        filename="simulador.log",
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )


def main():
    configurar_logging()

    # Perguntar ao iniciar se deseja carregar o times.csv
    mostrar_titulo("Bem-vindo ao simulador de CS2!")

    if confirmar_acao("Deseja carregar o arquivo times.csv ao iniciar?"):
        try:
            carregar_times_csv()  # Carrega o arquivo padrão
            df_jogadores = carregar_jogadores_de_arquivo("jogadores.csv")
            if df_jogadores is None:
                print(
                    "⚠️ 'jogadores.csv' não encontrado — os times foram carregados, mas sem elenco.\n"
                )
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"Arquivo 'times.csv' não encontrado no diretório atual!\n")

    while True:
        mostrar_titulo("Simulador de CS2\n")
        print("1. Gerenciar Times")
        print("2. Jogar Partida")
        print("3. Torneios")
        print("4. Carregar Times")
        print("5. Modo Carreira")
        print("6. Sair")

        escolha = obter_opcao_numerica(1, 6)

        if escolha == 1:
            menu_gerenciar_times()
        elif escolha == 2:
            menu_partida()
        elif escolha == 3:
            menu_torneio()
        elif escolha == 4:
            arquivo = input("Caminho do arquivo para carregar: ").strip()
            carregar_times_csv(arquivo)
        elif escolha == 5:
            menu_carreira()
        elif escolha == 6:
            if confirmar_acao("Tem certeza que deseja sair?"):
                print("Saindo...")
                break


if __name__ == "__main__":
    main()
