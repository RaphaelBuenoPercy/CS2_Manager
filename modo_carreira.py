import json
import random
import pandas as pd
from funcoes_torneio_deepseek import (
    fase_mata_mata,
    salvar_estatisticas_torneio,
    mostrar_resumo_torneio,
)
from funcoes_prejogo_deepseek import times, listar_times

# ===============================================================
# 1. CONFIGURAÇÕES GERAIS
# ===============================================================

CALENDARIO_TORNEIOS = {
    1: "IEM Los Angeles",
    2: "Blast Atenas",
    3: "ESL Pro League I Berlin",
    4: "Faceit Austin",
    5: "Blast Rivals Shangai",
    6: "IEM Bahia",
    7: "PGL Amsterdam Major",
    8: "Blast Atenas",
    9: "Thunderpick Malta",
    10: "Starladder Beijing",
    11: "ESL Pro League II Buenos Aires",
    12: "IEM New Orleans",
    13: "Faceit Madrid Major",
}

ARQUIVO_SAVE = "dados_carreira.json"

# ===============================================================
# 2. FUNÇÕES DE SALVAMENTO E CARREGAMENTO
# ===============================================================


def salvar_progresso(dados, arquivo=ARQUIVO_SAVE):
    """Salva o estado atual da carreira no arquivo JSON."""
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)
    print("💾 Progresso salvo com sucesso!\n")


def carregar_progresso(arquivo=ARQUIVO_SAVE):
    """Carrega o estado da carreira do arquivo JSON (ou cria padrão)."""
    try:
        with open(arquivo, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("⚠️ Nenhum save encontrado. Criando novo progresso.")
        return {
            "time_usuario": None,
            "ano_atual": 2026,
            "mes_atual": 1,
            "historico": [],
            "orcamento": 200000,
            "vitorias": 0,
            "derrotas": 0,
            "estatisticas": {},
        }


# ===============================================================
# 3. FUNÇÕES DE PROGRESSO TEMPORAL
# ===============================================================


def avancar_mes(dados):
    """Avança o mês e o ano no calendário da carreira."""
    dados["mes_atual"] += 1
    if dados["mes_atual"] > 12:
        dados["mes_atual"] = 1
        dados["ano_atual"] += 1
        print(f"\n📆 Novo Ano: {dados['ano_atual']}!\n")
    else:
        print(f"\n📅 Avançando para o mês {dados['mes_atual']}...\n")


def escolher_time_carreira():
    """Permite o usuário escolher o time para iniciar a carreira."""
    listar_times()
    while True:
        nome = input("Escolha seu time para iniciar a carreira: ").strip()
        if nome in times:
            return nome
        print("Time inválido. Tente novamente.\n")


# ===============================================================
# 4. FUNÇÃO PRINCIPAL DE TORNEIO DO MODO CARREIRA
# ===============================================================


def jogar_torneio_carreira(dados):
    """Executa o torneio do mês (se houver) no modo carreira."""
    mes = dados["mes_atual"]

    if mes not in CALENDARIO_TORNEIOS:
        print("🕐 Nenhum torneio neste mês.")
        return

    nome_torneio = CALENDARIO_TORNEIOS[mes]
    print(f"\n🏆 Torneio do mês: {nome_torneio}")

    # Sorteia os times participantes
    times_disponiveis = random.sample(times, 8)
    if dados["time_usuario"] not in times_disponiveis:
        times_disponiveis[0] = dados["time_usuario"]

    print(f"\nTimes participantes: {', '.join(times_disponiveis)}")

    # Executa o torneio usando suas funções já prontas
    vencedor, resultados = fase_mata_mata(times_disponiveis, [])

    # === Estatísticas ===
    print("\n📊 Gerando estatísticas do torneio...")
    df_estat, df_total = salvar_estatisticas_torneio(resultados, {}, nome_torneio)
    mostrar_resumo_torneio(df_estat, df_total)

    # Converte DataFrame para JSON e adiciona ao save
    dados["estatisticas"][nome_torneio] = {
        "detalhadas": df_estat.to_dict(),
        "resumo": df_total.to_dict(),
    }

    # === Resultado final ===
    if isinstance(vencedor, list):
        vencedor = vencedor[0]

    posicao = 1 if vencedor == dados["time_usuario"] else random.randint(2, 8)
    if posicao == 1:
        dados["orcamento"] += 50000
        dados["vitorias"] += 1
        print(f"🎉 Seu time foi CAMPEÃO do {nome_torneio}!")
    else:
        dados["derrotas"] += 1
        print(f"📊 Seu time terminou em {posicao}º lugar.")

    dados["historico"].append(
        {
            "ano": dados["ano_atual"],
            "mes": mes,
            "torneio": nome_torneio,
            "posicao": posicao,
        }
    )

    # ✅ Mostra estatísticas logo após o torneio
    print("\n=== ESTATÍSTICAS DO TORNEIO ===")
    print(df_total)
    input("\nPressione ENTER para continuar...")


def mostrar_estatisticas_gerais(dados):
    """Mostra estatísticas acumuladas por torneio e jogadores."""
    if not dados.get("estatisticas"):
        print("Nenhum dado estatístico disponível ainda.\n")
        return

    print("\n📈 Estatísticas Gerais da Carreira 📈\n")
    for torneio, info in dados["estatisticas"].items():
        print(f"=== {torneio} ===")
        resumo_df = pd.DataFrame(info["resumo"])
        print(resumo_df)
        print("\n--- Estatísticas Detalhadas ---")
        detalhado_df = pd.DataFrame(info["detalhadas"])
        print(detalhado_df.head(10))  # Mostra os 10 primeiros
        print("=" * 50 + "\n")


# ===============================================================
# 5. FUNÇÃO PARA EXIBIR O HISTÓRICO DO TIME
# ===============================================================


def mostrar_historico(dados):
    """Mostra todos os torneios jogados e posições alcançadas."""
    print("\n=== HISTÓRICO DE TORNEIOS ===")
    if not dados["historico"]:
        print("Nenhum torneio jogado ainda.\n")
        return
    for h in dados["historico"]:
        print(f"{h['ano']}/{h['mes']:02d} - {h['torneio']}: {h['posicao']}º lugar")
    print("==============================\n")


# ===============================================================
# 6. MENU PRINCIPAL DO MODO CARREIRA
# ===============================================================


def menu_carreira():
    dados = carregar_progresso()

    if not dados["time_usuario"]:
        dados["time_usuario"] = escolher_time_carreira()
        print(f"\n🚀 Carreira iniciada com o time: {dados['time_usuario']}\n")

    while True:
        print("\n" + "=" * 60)
        print("               🌟 MODO CARREIRA 🌟")
        print("=" * 60)
        print(f"Ano: {dados['ano_atual']} | Mês: {dados['mes_atual']}")
        print(f"Time: {dados['time_usuario']} | 💰 Orçamento: ${dados['orcamento']}")
        print(f"🏅 Vitórias: {dados['vitorias']} | ❌ Derrotas: {dados['derrotas']}")
        print("\n1. Jogar próximo mês")
        print("2. Ver histórico de torneios")
        print("3. Ver estatísticas da carreira")
        print("4. Salvar e sair\n")

        try:
            escolha = int(input("Escolha uma opção: "))
        except ValueError:
            print("Entrada inválida.")
            continue

        if escolha == 1:
            jogar_torneio_carreira(dados)
            avancar_mes(dados)
        elif escolha == 2:
            mostrar_historico(dados)
        elif escolha == 3:
            mostrar_estatisticas_gerais(dados)
        elif escolha == 4:
            salvar_progresso(dados)
            break
        else:
            print("Opção inválida.")
