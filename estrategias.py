import random

# Estratégias específicas por mapa
estrategias_por_mapa = {
    "Mirage": {
        "tr": ["1. rush B", "2. controle meio", "3. execução A", "4. fake B"],
        "ct": ["1. stack a", "2. defesa padrão", "3. retake A", "4. agressiva B"]
    },
    "Inferno": {
        "tr": ["1. execução xuxa", "2. wrap a", "3. rush B", "4. fake A"],
        "ct": ["1. stack A", "2. controle meio", "3. defesa padrão", "4. retake B"]
    },
    "Dust2": {
        "tr": ["1. rush B", "2. execuçao varanda", "3. execução fundo a", "4. split b"],
        "ct": ["1. rush escuro", "2. defesa padrão", "3. forte varanda", "4. forte fundo a"]
    },
    "Nuke": {
        "tr": ["1. rush rampa", "2. rush fora secret", "3. rush casinha", "4. descer duto"],
        "ct": ["1. avanço rampa", "2. Forte A", "3. avanço fora", "4. Forte B"]
    },
    "Ancient": {
        "tr": ["1. rush B", "2. controle meio", "3. execução A", "4. fake B"],
        "ct": ["1. stack meio", "2. defesa padrão", "3. retake A", "4. agressiva B"]
    },
    "Anubis": {
        "tr": ["1. execução A", "2. controle meio", "3. rush B", "4. fake A"],
        "ct": ["1. stack A", "2. controle meio", "3. defesa padrão", "4. retake B"]
    },
    "Train": {
        "tr": ["1. execução A", "2. rush B", "3. controle meio", "4. fake A"],
        "ct": ["1. defesa padrão", "2. stack A", "3. retake B", "4. agressiva meio"]
    } 
}



# Estratégias e resultados
def estrategia_resultado(estrategia_ct, estrategia_tr):
    if estrategia_ct == estrategia_tr:
        return random.choice(["ct", "tr"])
    elif (estrategia_ct == "1" and estrategia_tr == "3") or \
         (estrategia_ct == "2" and estrategia_tr == "4") or \
         (estrategia_ct == "3" and estrategia_tr == "1") or \
         (estrategia_ct == "4" and estrategia_tr == "2"):
        return "ct"
    else:
        return "tr"