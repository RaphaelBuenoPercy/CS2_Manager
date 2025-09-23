import random

# Estratégias específicas por mapa
estrategias_por_mapa = {
    "Mirage": {
        "tr": ["Rush A", "Exec A", "Pop Palacio", "Split A (3 Liga, 1 Caverna e 1 Palacio)",
               "Split B 3-2 (3 L, 2 Tapete)", "Exec B", "Contato Tapete"],
        "ct": ["Soft A", "Batida 2 Palacio", "Setup A: 1 Areia 1 Sanduiche", "Batida Meio (2 Rushando Top Mid, 1 Olhando Rato)",
                "Boost no Overdrive", "Setup B: 2L", "Default"]
    },
    "Dust2": {
        "tr": ["Rush Rapido B", "Exec B", "Split B", "Rapido Varanda", "Exec Varanda", "Fundo A Rápido",
               "Fundo A Lento"],
        "ct": ["2-1-2 (2 B, 1 Meio, 2 A)", "Avanço Escuro Alto em 2", "Setup B: 1 Bomb e 1 Altar", "Batida Meio", "2 Varanda", "Dominio Fundo A",
               "1-4 (1 B, 2 Varanda e 2 Fundo A)"]
    },
    "Inferno": {
        "tr": ["Pop B", "Exec B", "Split B (3 NIP, 2 Banana)", "Exec A (Xuxa e Tapete)", "Split A (2 Nip, 2 Xuxa, 1 Tapete)", "Pop Tapete"],
        "ct": ["Batida Banana", "Setup B: Flash do BTT, abre o BTT e o Caixão na flash", "Soft B", "Bait Peru", "Avanço Campa", "Double Bomb A",
               " Default"]
    },
    "Nuke": {
        "tr": ["Rush Rampa B", "Split B (2 Rampa, 3 Secret)", "Descida Duto", "Passagem Secret", "Pop A", "Rush Rapido Terra",
               "Exec A"],
        "ct": ["Bait Rampa", "Soft Rampa (2 Fora, 2 A, 1 Cat)", "Bait B (1 Reator e 1 Quina)", "Batida Miolo", "2 Secret", "3 A", "Default"]
    },
    "Ancient": {
        "tr": ["Pop A", "Exec A", "Split A", "Pop Caverna", "Split B (2 Caverna e 3 Rampa)", "Contato Rampa", "Exec B"],
        "ct": ["Bait Árvore", "Soft A", "Double Quadrado", "Batida Meio", "Double Caverna", "Soft B", "Default"]
    },
    "Anubis": {
        "tr": ["Rush B", "Exec B", "Split B (2 Fundo e 3 Rato)", "Rush Caverna", "Pop Mid A", "Split A (3 Mid A, 2 Fundo A)", "Exec Fundo A",
               "Contato A"],
        "ct": ["Batida Fundo B", "Double Rato", "Cruzado Fundo B", "Bait Meio", "Batida Meio Água e Rato", "Soft A", "Batida Fundo A"]
    },
    "Train": {
        "tr": ["Rush Fundo A", "Rush Fundo pra B", "Split A (2 Fundo, 2 Meio, 1 Bombeiro)", "Exec A Meio", "Pop Bombeiro", "Exec B", "Pop B"],
        "ct": ["Cruzado Fundo", "Batida Meio", "Give Meio e Bombeiro (Jogar pelo Bomb e Fundo)", "Batida Bombeiro", "Double Gaules", "Batida B",
               "Soft B"]
    },
}



# Estratégias e resultados
regras_vitoria_por_mapa = {
    "Mirage": {
        "ct_vence": [
            ("1", "1"),  # CT ganha se CT escolher estratégia 1 e TR escolher estratégia 1
            ("1", "3"),  # CT ganha se CT escolher estratégia 1 e TR escolher estratégia 3
            ("1", "5"),  # CT ganha se CT escolher estratégia 1 e TR escolher estratégia 5
            ("2", "2"),   # CT ganha se CT escolher estratégia 2 e TR escolher estratégia 2
            ("2", "4"),   # CT ganha se CT escolher estratégia 2 e TR escolher estratégia 4
            ("2", "6"),   # CT ganha se CT escolher estratégia 2 e TR escolher estratégia 6
            ("3", "1"),   # CT ganha se CT escolher estratégia 3 e TR escolher estratégia 1
            ("3", "2"),   # CT ganha se CT escolher estratégia 3 e TR escolher estratégia 2
            ("4", "4"),   # CT ganha se CT escolher estratégia 4 e TR escolher estratégia 4
            ("4", "5"),   # CT ganha se CT escolher estratégia 4 e TR escolher estratégia 5
            ("5", "6"),   # CT ganha se CT escolher estratégia 5 e TR escolher estratégia 6
            ("5", "7"),   # CT ganha se CT escolher estratégia 5 e TR escolher estratégia 7
            ("6", "5"),   # CT ganha se CT escolher estratégia 6 e TR escolher estratégia 5
            ("6", "7"),   # CT ganha se CT escolher estratégia 6 e TR escolher estratégia 7
        ],
        "tr_vence": [
            ("1", "2"),  # CT ganha se CT escolher estratégia 1 e TR escolher estratégia 2
            ("1", "4"),  # CT ganha se CT escolher estratégia 1 e TR escolher estratégia 4
            ("2", "1"),   # CT ganha se CT escolher estratégia 2 e TR escolher estratégia 1
            ("2", "3"),   # CT ganha se CT escolher estratégia 2 e TR escolher estratégia 3
            ("3", "3"),   # CT ganha se CT escolher estratégia 3 e TR escolher estratégia 3
            ("3", "4"),   # CT ganha se CT escolher estratégia 3 e TR escolher estratégia 4
            ("3", "5"),   # CT ganha se CT escolher estratégia 3 e TR escolher estratégia 5
            ("4", "1"),   # CT ganha se CT escolher estratégia 4 e TR escolher estratégia 1
            ("4", "7"),   # CT ganha se CT escolher estratégia 4 e TR escolher estratégia 7
            ("5", "5"),   # CT ganha se CT escolher estratégia 5 e TR escolher estratégia 5
            ("6", "2"),   # CT ganha se CT escolher estratégia 6 e TR escolher estratégia 2
            ("6", "6"),   # CT ganha se CT escolher estratégia 6 e TR escolher estratégia 6
        ]
    },
    "Dust2": {
        "ct_vence": [
            ("1", "1"),  # CT ganha se CT escolher estratégia 1 e TR escolher estratégia 1
            ("1", "3"),  # CT ganha se CT escolher estratégia 1 e TR escolher estratégia 3
            ("2", "3"),  # CT ganha se CT escolher estratégia 2 e TR escolher estratégia 3
            ("2", "5"),   # CT ganha se CT escolher estratégia 2 e TR escolher estratégia 5
            ("2", "7"),   # CT ganha se CT escolher estratégia 2 e TR escolher estratégia 7
            ("3", "1"),   # CT ganha se CT escolher estratégia 3 e TR escolher estratégia 1
            ("3", "2"),   # CT ganha se CT escolher estratégia 3 e TR escolher estratégia 2
            ("4", "4"),   # CT ganha se CT escolher estratégia 4 e TR escolher estratégia 4
            ("4", "5"),   # CT ganha se CT escolher estratégia 4 e TR escolher estratégia 5
            ("4", "7"),   # CT ganha se CT escolher estratégia 4 e TR escolher estratégia 7
            ("5", "2"),   # CT ganha se CT escolher estratégia 5 e TR escolher estratégia 2
            ("5", "4"),   # CT ganha se CT escolher estratégia 5 e TR escolher estratégia 4
            ("5", "5"),   # CT ganha se CT escolher estratégia 5 e TR escolher estratégia 5
            ("6", "6"),   # CT ganha se CT escolher estratégia 6 e TR escolher estratégia 6
            ("6", "7"),   # CT ganha se CT escolher estratégia 6 e TR escolher estratégia 7
            ("7", "6"),   # CT ganha se CT escolher estratégia 6 e TR escolher estratégia 6
            ("7", "7"),   # CT ganha se CT escolher estratégia 6 e TR escolher estratégia 7
        ],
        "tr_vence": [
            ("1", "6"),  # CT ganha se CT escolher estratégia 1 e TR escolher estratégia 2
            ("1", "7"),  # CT ganha se CT escolher estratégia 1 e TR escolher estratégia 4
            ("2", "2"),   # CT ganha se CT escolher estratégia 2 e TR escolher estratégia 1
            ("2", "4"),   # CT ganha se CT escolher estratégia 2 e TR escolher estratégia 3
            ("2", "6"),   # CT ganha se CT escolher estratégia 3 e TR escolher estratégia 3
            ("3", "3"),   # CT ganha se CT escolher estratégia 3 e TR escolher estratégia 4
            ("3", "5"),   # CT ganha se CT escolher estratégia 3 e TR escolher estratégia 5
            ("4", "1"),   # CT ganha se CT escolher estratégia 4 e TR escolher estratégia 1
            ("4", "2"),   # CT ganha se CT escolher estratégia 4 e TR escolher estratégia 7
            ("4", "6"),   # CT ganha se CT escolher estratégia 4 e TR escolher estratégia 5
            ("5", "1"),   # CT ganha se CT escolher estratégia 5 e TR escolher estratégia 2
            ("5", "7"),   # CT ganha se CT escolher estratégia 5 e TR escolher estratégia 6
            ("6", "2"),   # CT ganha se CT escolher estratégia 6 e TR escolher estratégia 5
            ("6", "3"),   # CT ganha se CT escolher estratégia 6 e TR escolher estratégia 2
            ("6", "4"),   # CT ganha se CT escolher estratégia 6 e TR escolher estratégia 6
            ("6", "5"),   # CT ganha se CT escolher estratégia 6 e TR escolher estratégia 5
            ("7", "1"),   # CT ganha se CT escolher estratégia 7 e TR escolher estratégia 5
            ("7", "3"),   # CT ganha se CT escolher estratégia 7 e TR escolher estratégia 2
        ]
    },
    "Inferno": {
        "ct_vence": [
            ("1", "1"),  # CT ganha se CT escolher estratégia 1 e TR escolher estratégia 1
            ("1", "3"),  # CT ganha se CT escolher estratégia 1 e TR escolher estratégia 3
            ("2", "2"),  # CT ganha se CT escolher estratégia 2 e TR escolher estratégia 2
            ("2", "3"),   # CT ganha se CT escolher estratégia 2 e TR escolher estratégia 3
            ("3", "1"),  # CT ganha se CT escolher estratégia 3 e TR escolher estratégia 1
            ("3", "2"),  # CT ganha se CT escolher estratégia 3 e TR escolher estratégia 2
            ("3", "4"),  # CT ganha se CT escolher estratégia 3 e TR escolher estratégia 4
            ("4", "5"),   # CT ganha se CT escolher estratégia 4 e TR escolher estratégia 5
            ("5", "4"),  # CT ganha se CT escolher estratégia 5 e TR escolher estratégia 4
            ("5", "6"),  # CT ganha se CT escolher estratégia 5 e TR escolher estratégia 6
            ("6", "4"),  # CT ganha se CT escolher estratégia 6 e TR escolher estratégia 4
            ("6", "6"),   # CT ganha se CT escolher estratégia 6 e TR escolher estratégia 6
        ],
        "tr_vence": [
            ("1", "2"),  # TR ganha se CT escolher estratégia 1 e TR escolher estratégia 2
            ("1", "4"),  # TR ganha se CT escolher estratégia 1 e TR escolher estratégia 4
            ("2", "1"),  # TR ganha se CT escolher estratégia 2 e TR escolher estratégia 1
            ("3", "3"),   # TR ganha se CT escolher estratégia 3 e TR escolher estratégia 3
            ("3", "6"),  # TR ganha se CT escolher estratégia 3 e TR escolher estratégia 6
            ("4", "1"),   # TR ganha se CT escolher estratégia 4 e TR escolher estratégia 1
            ("4", "4"),  # TR ganha se CT escolher estratégia 4 e TR escolher estratégia 4
            ("4", "6"),  # TR ganha se CT escolher estratégia 4 e TR escolher estratégia 6
            ("5", "3"),  # TR ganha se CT escolher estratégia 5 e TR escolher estratégia 3
            ("5", "5"),   # TR ganha se CT escolher estratégia 5 e TR escolher estratégia 5
            ("6", "2"),  # TR ganha se CT escolher estratégia 6 e TR escolher estratégia 2
            ("6", "3"),  # TR ganha se CT escolher estratégia 6 e TR escolher estratégia 3
            ("6", "5"),  # TR ganha se CT escolher estratégia 6 e TR escolher estratégia 3
        ]
    },
    "Nuke": {
        "ct_vence": [
            ("1", "1"),  # CT ganha se CT escolher estratégia 1 e TR escolher estratégia 1
            ("1", "4"),  # CT ganha se CT escolher estratégia 2 e TR escolher estratégia 4
            ("2", "2"),  # CT ganha se CT escolher estratégia 3 e TR escolher estratégia 2
            ("2", "5"),  # CT ganha se CT escolher estratégia 4 e TR escolher estratégia 5
            ("2", "6"),  # CT ganha se CT escolher estratégia 4 e TR escolher estratégia 6
            ("3", "1"),  # CT ganha se CT escolher estratégia 1 e TR escolher estratégia 1
            ("3", "3"),  # CT ganha se CT escolher estratégia 2 e TR escolher estratégia 3
            ("3", "4"),  # CT ganha se CT escolher estratégia 3 e TR escolher estratégia 4
            ("4", "5"),  # CT ganha se CT escolher estratégia 4 e TR escolher estratégia 5
            ("5", "2"),  # CT ganha se CT escolher estratégia 1 e TR escolher estratégia 2
            ("5", "4"),  # CT ganha se CT escolher estratégia 2 e TR escolher estratégia 4
            ("6", "6"),  # CT ganha se CT escolher estratégia 3 e TR escolher estratégia 6
            ("6", "7"),   # CT ganha se CT escolher estratégia 4 e TR escolher estratégia 7
        ],
        "tr_vence": [
            ("1", "3"),  # TR ganha se CT escolher estratégia 1 e TR escolher estratégia 3
            ("1", "5"),  # TR ganha se CT escolher estratégia 1 e TR escolher estratégia 5
            ("1", "6"),  # TR ganha se CT escolher estratégia 1 e TR escolher estratégia 6
            ("2", "1"),  # TR ganha se CT escolher estratégia 2 e TR escolher estratégia 1
            ("2", "7"),   # TR ganha se CT escolher estratégia 2 e TR escolher estratégia 7
            ("3", "2"),  # TR ganha se CT escolher estratégia 3 e TR escolher estratégia 2
            ("3", "4"),   # TR ganha se CT escolher estratégia 3 e TR escolher estratégia 4
            ("4", "4"),  # TR ganha se CT escolher estratégia 4 e TR escolher estratégia 4
            ("4", "6"),  # TR ganha se CT escolher estratégia 4 e TR escolher estratégia 6
            ("5", "3"),  # TR ganha se CT escolher estratégia 5 e TR escolher estratégia 3
            ("5", "5"),   # TR ganha se CT escolher estratégia 5 e TR escolher estratégia 5
            ("6", "1"),  # TR ganha se CT escolher estratégia 6 e TR escolher estratégia 1
            ("6", "2"),  # TR ganha se CT escolher estratégia 6 e TR escolher estratégia 2
        ]
    },
    "Ancient": {
        "ct_vence": [
            ("1", "1"),  # CT ganha se CT escolher estratégia 1 e TR escolher estratégia 4
            ("1", "2"),  # CT ganha se CT escolher estratégia 2 e TR escolher estratégia 1
            ("2", "3"),  # CT ganha se CT escolher estratégia 3 e TR escolher estratégia 2
            ("2", "5"),   # CT ganha se CT escolher estratégia 4 e TR escolher estratégia 3
            ("3", "1"),   # CT ganha se CT escolher estratégia 4 e TR escolher estratégia 3
            ("3", "3"),  # CT ganha se CT escolher estratégia 1 e TR escolher estratégia 4
            ("4", "2"),  # CT ganha se CT escolher estratégia 2 e TR escolher estratégia 1
            ("4", "5"),  # CT ganha se CT escolher estratégia 3 e TR escolher estratégia 2
            ("4", "6"),   # CT ganha se CT escolher estratégia 4 e TR escolher estratégia 3
            ("5", "4"),  # CT ganha se CT escolher estratégia 1 e TR escolher estratégia 4
            ("5", "5"),  # CT ganha se CT escolher estratégia 2 e TR escolher estratégia 1
            ("6", "6"),   # CT ganha se CT escolher estratégia 4 e TR escolher estratégia 3
            ("6", "7"),   # CT ganha se CT escolher estratégia 4 e TR escolher estratégia 3
        ],
        "tr_vence": [
            ("1", "3"),  # TR ganha se CT escolher estratégia 1 e TR escolher estratégia 2
            ("1", "6"),  # TR ganha se CT escolher estratégia 2 e TR escolher estratégia 3
            ("2", "1"),  # TR ganha se CT escolher estratégia 2 e TR escolher estratégia 3
            ("2", "2"),  # TR ganha se CT escolher estratégia 3 e TR escolher estratégia 4
            ("3", "2"),   # TR ganha se CT escolher estratégia 4 e TR escolher estratégia 1
            ("3", "7"),  # TR ganha se CT escolher estratégia 3 e TR escolher estratégia 4
            ("4", "1"),   # TR ganha se CT escolher estratégia 4 e TR escolher estratégia 1
            ("4", "4"),  # TR ganha se CT escolher estratégia 1 e TR escolher estratégia 2
            ("4", "5"),  # TR ganha se CT escolher estratégia 1 e TR escolher estratégia 2
            ("5", "6"),  # TR ganha se CT escolher estratégia 2 e TR escolher estratégia 3
            ("5", "7"),  # TR ganha se CT escolher estratégia 3 e TR escolher estratégia 4
            ("6", "3"),   # TR ganha se CT escolher estratégia 4 e TR escolher estratégia 1
            ("6", "5"),  # TR ganha se CT escolher estratégia 2 e TR escolher estratégia 3
        ]
    },
    "Anubis": {
        "ct_vence": [
            ("1", "1"),  # CT ganha se CT escolher estratégia 1 e TR escolher estratégia 4
            ("1", "2"),  # CT ganha se CT escolher estratégia 2 e TR escolher estratégia 1
            ("2", "3"),  # CT ganha se CT escolher estratégia 3 e TR escolher estratégia 2
            ("2", "4"),   # CT ganha se CT escolher estratégia 4 e TR escolher estratégia 3
            ("3", "1"),   # CT ganha se CT escolher estratégia 4 e TR escolher estratégia 3
            ("4", "5"),  # CT ganha se CT escolher estratégia 2 e TR escolher estratégia 1
            ("4", "6"),  # CT ganha se CT escolher estratégia 3 e TR escolher estratégia 2
            ("5", "3"),   # CT ganha se CT escolher estratégia 4 e TR escolher estratégia 3
            ("5", "4"),  # CT ganha se CT escolher estratégia 1 e TR escolher estratégia 4
            ("5", "7"),  # CT ganha se CT escolher estratégia 2 e TR escolher estratégia 1
            ("6", "5"),   # CT ganha se CT escolher estratégia 4 e TR escolher estratégia 3
            ("6", "7"),   # CT ganha se CT escolher estratégia 4 e TR escolher estratégia 3
            ("7", "2"),   # CT ganha se CT escolher estratégia 4 e TR escolher estratégia 3
            ("7", "6"),   # CT ganha se CT escolher estratégia 4 e TR escolher estratégia 3
        ],
        "tr_vence": [
            ("1", "3"),  # TR ganha se CT escolher estratégia 1 e TR escolher estratégia 2
            ("1", "4"),  # TR ganha se CT escolher estratégia 2 e TR escolher estratégia 3
            ("1", "6"),  # TR ganha se CT escolher estratégia 2 e TR escolher estratégia 3
            ("2", "1"),  # TR ganha se CT escolher estratégia 2 e TR escolher estratégia 3
            ("2", "2"),  # TR ganha se CT escolher estratégia 3 e TR escolher estratégia 4
            ("2", "7"),  # TR ganha se CT escolher estratégia 2 e TR escolher estratégia 3
            ("3", "2"),   # TR ganha se CT escolher estratégia 4 e TR escolher estratégia 1
            ("3", "4"),  # TR ganha se CT escolher estratégia 3 e TR escolher estratégia 4
            ("3", "7"),  # TR ganha se CT escolher estratégia 2 e TR escolher estratégia 3
            ("4", "1"),   # TR ganha se CT escolher estratégia 4 e TR escolher estratégia 1
            ("4", "3"),  # TR ganha se CT escolher estratégia 1 e TR escolher estratégia 2
            ("4", "7"),  # TR ganha se CT escolher estratégia 2 e TR escolher estratégia 3
            ("5", "1"),  # TR ganha se CT escolher estratégia 1 e TR escolher estratégia 2
            ("5", "5"),  # TR ganha se CT escolher estratégia 2 e TR escolher estratégia 3
            ("5", "6"),  # TR ganha se CT escolher estratégia 2 e TR escolher estratégia 3
            ("6", "3"),  # TR ganha se CT escolher estratégia 3 e TR escolher estratégia 4
            ("6", "4"),   # TR ganha se CT escolher estratégia 4 e TR escolher estratégia 1
            ("6", "6"),   # TR ganha se CT escolher estratégia 4 e TR escolher estratégia 1
            ("7", "2"),  # TR ganha se CT escolher estratégia 2 e TR escolher estratégia 3
            ("7", "5"),  # TR ganha se CT escolher estratégia 2 e TR escolher estratégia 3
        ]
    },
    "Train": {
        "ct_vence": [
            ("1", "1"),  # CT ganha se CT escolher estratégia 1 e TR escolher estratégia 1
            ("1", "2"),  # CT ganha se CT escolher estratégia 1 e TR escolher estratégia 2
            ("2", "3"),  # CT ganha se CT escolher estratégia 2 e TR escolher estratégia 3
            ("2", "4"),   # CT ganha se CT escolher estratégia 2 e TR escolher estratégia 4
            ("3", "2"),   # CT ganha se CT escolher estratégia 3 e TR escolher estratégia 2
            ("3", "5"),  # CT ganha se CT escolher estratégia 3 e TR escolher estratégia 5
            ("4", "1"),  # CT ganha se CT escolher estratégia 4 e TR escolher estratégia 1
            ("4", "3"),  # CT ganha se CT escolher estratégia 4 e TR escolher estratégia 3
            ("4", "5"),   # CT ganha se CT escolher estratégia 4 e TR escolher estratégia 5
            ("5", "4"),  # CT ganha se CT escolher estratégia 5 e TR escolher estratégia 4
            ("5", "7"),  # CT ganha se CT escolher estratégia 5 e TR escolher estratégia 7
            ("6", "6"),  # CT ganha se CT escolher estratégia 6 e TR escolher estratégia 6
            ("6", "7"),   # CT ganha se CT escolher estratégia 6 e TR escolher estratégia 7
            ("7", "6"),   # CT ganha se CT escolher estratégia 7 e TR escolher estratégia 6
        ],
        "tr_vence": [
            ("1", "4"),  # TR ganha se CT escolher estratégia 1 e TR escolher estratégia 4
            ("1", "5"),  # TR ganha se CT escolher estratégia 1 e TR escolher estratégia 5
            ("2", "1"),  # TR ganha se CT escolher estratégia 2 e TR escolher estratégia 1
            ("2", "2"),  # TR ganha se CT escolher estratégia 2 e TR escolher estratégia 2
            ("3", "3"),   # TR ganha se CT escolher estratégia 3 e TR escolher estratégia 3
            ("3", "4"),  # TR ganha se CT escolher estratégia 3 e TR escolher estratégia 4
            ("4", "2"),   # TR ganha se CT escolher estratégia 4 e TR escolher estratégia 2
            ("4", "5"),  # TR ganha se CT escolher estratégia 4 e TR escolher estratégia 5
            ("4", "6"),  # CT ganha se CT escolher estratégia 4 e TR escolher estratégia 6
            ("5", "5"),  # TR ganha se CT escolher estratégia 5 e TR escolher estratégia 5
            ("5", "6"),  # TR ganha se CT escolher estratégia 5 e TR escolher estratégia 6
            ("6", "2"),   # TR ganha se CT escolher estratégia 6 e TR escolher estratégia 2
            ("6", "3"),  # TR ganha se CT escolher estratégia 6 e TR escolher estratégia 3
            ("7", "1"),  # CT ganha se CT escolher estratégia 7 e TR escolher estratégia 1
        ]
    },
    # Adicione mais mapas e regras conforme necessário
}

def estrategia_resultado(estrategia_ct: str, estrategia_tr: str, mapa: str) -> str:
    """
    Decide o vencedor do round com base nas estratégias escolhidas e no mapa.

    Args:
        estrategia_ct: Estratégia escolhida pelo time CT.
        estrategia_tr: Estratégia escolhida pelo time TR.
        mapa: Mapa em que o round está sendo jogado.

    Returns:
        "ct" se o time CT vencer, "tr" se o time TR vencer.
    """
    # Verifica se o mapa tem regras específicas
    if mapa not in regras_vitoria_por_mapa:
        raise ValueError(f"Mapa '{mapa}' não encontrado nas regras de vitória")

    # Obtém as regras de vitória para o mapa
    regras_ct = regras_vitoria_por_mapa[mapa]["ct_vence"]
    regras_tr = regras_vitoria_por_mapa[mapa]["tr_vence"]

    # Verifica se o CT vence
    if (estrategia_ct, estrategia_tr) in regras_ct:
        return "ct"

    # Verifica se o TR vence
    if (estrategia_ct, estrategia_tr) in regras_tr:
        return "tr"

    # Caso não haja regra específica, decide aleatoriamente
    return random.choice(["ct", "tr"])

