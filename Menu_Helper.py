import random
from funcoes_torneio_deepseek import criar_torneio
from funcoes_prejogo_deepseek import times, listar_times, carregar_times_csv, adicionar_time, calcular_overs_medios_times, exibir_overs_medios_times
from funcoes_simulacao_deepseek import jogar_partida

# ==================== FUNÇÕES AUXILIARES ====================
def mostrar_titulo(texto: str):
    """Exibe títulos formatados"""
    print("\n" + "="*50)
    print(f" {texto.upper()} ".center(50, "•"))
    print("="*50 + "\n")

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
    return resposta in ['s', 'sim']

# ==================== SUBMENUS ====================
def menu_gerenciar_times():
    """Submenu para gestão de times"""
    while True:
        mostrar_titulo("gestão de times")
        print("1. Adicionar time")
        print("2. Remover time")
        print("3. Listar times")
        print("4. Calcular Overs dos Times")
        print("5. Voltar ao menu principal")
        
        escolha = obter_opcao_numerica(1, 4)
        
        if escolha == 1:
            nome = input("Nome do novo time: ").strip()
            adicionar_time(nome)
        elif escolha == 2:
            listar_times()
            if times:
                try:
                    idx = int(input("Número do time a remover: ")) - 1
                    if 0 <= idx < len(times):
                        if confirmar_acao("Tem certeza que deseja remover este time?"):
                            removed = times.pop(idx)
                            print(f"Time {removed} removido!")
                except ValueError:
                    print("Número inválido!")
        elif escolha == 3:
            listar_times()
        elif escolha == 4:
            calcular_overs_medios_times()
            exibir_overs_medios_times()
        elif escolha == 5:
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
                jogar_partida(modo='auto', time1=time1, time2=time2)
            else:
                print("Necessário pelo menos 2 times registrados!")
        elif escolha == 2:
            if len(times) >= 2:
                listar_times()
                time1 = input("Nome do primeiro time: ").strip()
                time2 = input("Nome do segundo time: ").strip()
                if time1 in times and time2 in times:
                    jogar_partida(modo='manual', time1=time1, time2=time2)
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
        print("3. Voltar ao menu principal")
        
        escolha = obter_opcao_numerica(1, 3)
        
        if escolha == 1:
            criar_torneio(times)
        elif escolha == 2:
            # Implementar listagem de torneios
            print("Funcionalidade em desenvolvimento!")
        elif escolha == 3:
            return

# ==================== MENU PRINCIPAL ====================
def main():
    # Perguntar ao iniciar se deseja carregar o times.csv
    mostrar_titulo("Bem-vindo ao simulador de CS2!")
    if confirmar_acao("Deseja carregar o arquivo times.csv ao iniciar?"):
        try:
            carregar_times_csv()  # Carrega o arquivo padrão
        except FileNotFoundError:
            print(f"Arquivo 'times.csv' não encontrado no diretório atual!\n")

    while True:
        mostrar_titulo("Simulador de CS2\n")
        print("1. Gerenciar Times")
        print("2. Jogar Partida")
        print("3. Torneios")
        print("4. Carregar Times")
        print("5. Sair")

        escolha = obter_opcao_numerica(1, 5)

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
            if confirmar_acao("Tem certeza que deseja sair?"):
                print("Saindo...")
                break

if __name__ == "__main__":
    main()