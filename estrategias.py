import random

# Estratégias específicas por mapa
estrategias_por_mapa = {
    "Mirage": {
        "tr": ["rush B", "controle meio", "execução A", "fake B"],
        "ct": ["stack a", "defesa padrão", "retake A", "agressiva B"]
    },
    "Inferno": {
        "tr": ["execução xuxa", "wrap a", "rush B", "fake A"],
        "ct": ["stack A", "controle meio", "defesa padrão", "retake B"]
    },
    "Dust2": {
        "tr": ["rush B", "execuçao varanda", "execução fundo a", "split b"],
        "ct": ["rush escuro", "defesa padrão", "forte varanda", "forte fundo a"]
    },
    "Nuke": {
        "tr": ["rush rampa", "rush fora secret", "rush casinha", "descer duto"],
        "ct": ["avanço rampa", "Forte A", "avanço fora", "Forte B"]
    },
    "Ancient": {
        "tr": ["rush B", "controle meio", "execução A", "fake B"],
        "ct": ["stack meio", "defesa padrão", "retake A", "agressiva B"]
    },
    "Anubis": {
        "tr": ["execução A", "controle meio", "rush B", "fake A"],
        "ct": ["stack A", "controle meio", "defesa padrão", "retake B"]
    },
    "Train": {
        "tr": ["execução A", "rush B", "controle meio", "fake A"],
        "ct": ["defesa padrão", "stack A", "retake B", "agressiva meio"]
    } 
}



# Estratégias e resultados
def estrategia_resultado(estrategia_ct, estrategia_tr):
    estrategia_ct = str(estrategia_ct)
    estrategia_tr = str(estrategia_tr)

    if estrategia_ct == estrategia_tr:
        return random.choice(["ct", "tr"])
    elif (estrategia_ct == "1" and estrategia_tr == "3") or \
         (estrategia_ct == "2" and estrategia_tr == "4") or \
         (estrategia_ct == "3" and estrategia_tr == "1") or \
         (estrategia_ct == "4" and estrategia_tr == "2"):
        return "ct"
    else:
        return "tr"