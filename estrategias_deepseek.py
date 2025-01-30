import random

# Estratégias específicas por mapa
estrategias_por_mapa = {
    "Inferno": {
        "tr": {
            "inicio": ["1. Peek Banana", "2. Dominio Banana", "3. Dominio Meio", "4. Dominio Campa", "5. Default"],
            "meio": ["1. Rush B", "2. Rush Xuxa", "3. Rush Tapete", "4. Causar B", "5. Baitar Utility B", "6. Exec B", "7. Brigar Nip",
                    "8. Ganhar Campa", "9. Redominar Banana Full", "10. Redominar Banana Safe", "11. Exec Xuxa", "12. Dominar Meio",
                    "13. Causar Meio", "14. Peek Tapete", "15. Pop Tapete Light", "16. Redominar Meio", "17. Redominar Campa",
                    "18. Baitar Utility A"],
            "fim": ["1. Exec B", "2. Split B", "3. Contato B", "4. Exec Xuxa_Tapete", "5. Exec Nip_Xuxa", "6. Wrap A",
                    "7. Pop Tapete", "8. Fake B", "9. Fake A"] 
        },
        "ct": {
            "inicio": ["1. Utilty Banana Safe", "2. Utility Banana Pesada", "3. Batida Banana", "4. Peek Meio", "5. Rush Meio", "6. 3 Meio",
                       "7. Avanço Campa", "8. Default"],
            "meio": ["1. Redominio Banana", "2. Retake B", "3. Defesa Forte B", "4. Bait Nip", "5. Safe Meio", "6. Pezinho Cogu",
                     "7. Double Campa", "8. Jogar do Bomb A", "9. Defesa Forte A", "10. Areia Forte", "11. Stack A", "12. Stack B"],
            "fim": ["1. Retake B", "2. Defesa B", "3. Tripla_Newba", "4. 3 Meio", "5. Xuxa", "6. Retake A", "7. Double Bomb A",
                    "8. Telha_Areia", "9. Areia Forte", "10. Forte A", "11. Forte B", "12. Stack A", "13. Stack B"]
        }
    },
    "Mirage": {
        "tr": {
            "inicio": ["1. Peek Banana", "2. Dominio Banana", "3. Dominio Meio", "4. Dominio Campa", "5. Default"],
            "meio": ["1. Rush B", "2. Rush Xuxa", "3. Rush Tapete", "4. Causar B", "5. Baitar Utility B", "6. Exec B", "7. Brigar Nip",
                    "8. Ganhar Campa", "9. Redominar Banana Full", "10. Redominar Banana Safe", "11. Exec Xuxa", "12. Dominar Meio",
                    "13. Causar Meio", "14. Peek Tapete", "15. Pop Tapete Light", "16. Redominar Meio", "17. Redominar Campa",
                    "18. Baitar Utility A"],
            "fim": ["1. Exec B", "2. Split B", "3. Contato B", "4. Exec Xuxa_Tapete", "5. Exec Nip_Xuxa", "6. Wrap A",
                    "7. Pop Tapete", "8. Fake B", "9. Fake A"] 
        },
        "ct": {
            "inicio": ["1. Utilty Banana Safe", "2. Utility Banana Pesada", "3. Batida Banana", "4. Peek Meio", "5. Rush Meio", "6. 3 Meio",
                       "7. Avanço Campa", "8. Default"],
            "meio": ["1. Redominio Banana", "2. Retake B", "3. Defesa Forte B", "4. Bait Nip", "5. Safe Meio", "6. Pezinho Cogu",
                     "7. Double Campa", "8. Jogar do Bomb A", "9. Defesa Forte A", "10. Areia Forte", "11. Stack A", "12. Stack B"],
            "fim": ["1. Retake B", "2. Defesa B", "3. Tripla_Newba", "4. 3 Meio", "5. Xuxa", "6. Retake A", "7. Double Bomb A",
                    "8. Telha_Areia", "9. Areia Forte", "10. Forte A", "11. Forte B", "12. Stack A", "13. Stack B"]
        }
    },
    "Dust 2": {
        "tr": {
            "inicio": ["1. Rush B", "2. Peek B", "3. Dominio Escuro Baixo", "4. Peek Meio", "5. Dominio Meio Baixo", "6. Dominio Varanda",
                       "7. Dominio Fundo", "8. Peek Fundo"],
            "meio": ["1. Rush B", "2. Exec B", "3. Bait Utility B", "4. Lurk Smoke B", "5. Dominio Meio Baixo", "6. Dominio Meio",
                     "7. Dominio Varanda", "8. Peek Porta", "9. Split B", "10. Rush Porta", "11. Exec Varanda Default",
                     "12. Exec Varanda Caindo Rampa", "13. Fake Varanda", "14. Dominio Fundo", "15. Peek Fundo", "16. Rush Fundo",
                     "17. Exec Fundo", "18. Baitar Utility Fundo"],
            "fim": ["1. Exec B", "2. Split B", "3. Contato B", "5. Fake Split B", "6. Exec Varanda Default", "7. Exec Varanda Caindo Rampa",
                    "8. Contato Varanda", "9. Wrap A", "10. Exec Fundo", "11. Contato Fundo"]
        },
        "ct": {
            "inicio": ["1. Anti-Rush B", "2. Avanço Escuro Baixo", "3. Dois Porta", "4. Rush Esquina", "5. Peek Varanda", "6. Dominio Fundo",
                       "7. Batida Fundo", "8. Default"],
            "meio": ["1. Avanço Escuro", "2. Forte B", "3. Double B olhando Meio e B", "4. Bait Porta", "5. Double Varanda", "6. Bait Varanda",
                     "7. Redominio Fundo", "8. Forte Varanda", "9. Forte Fundo", "10. Bait Fundo", "11. Safe A", "12. Stack A", "13; Stack B"],
            "fim": ["1. Bait B", "2. Forte B", "3. Retake B", "4. Double CT", "5. Forte Varanda", "6. Bait Bomb A", "7. Smoke Varanda",
                    "8. Forte A", "9. Forte Fundo", "10. Bait Fundo", "11. Retake Fundo", "12. Stack A", "13. Stack B", "14. Bunker"]
        }
    },
    "Nuke": {
        "tr": {
            "inicio": ["1. Rush Rampa B", "2. Peek Rampa", "3. Dominio Rampa", "4. Rush Casinha", "5. Peek Casinha", "6. Rush Porta",
                       "7. Peek Porta", "8. Rush Duto", "9. Rush Casinha + Porta", "10. Rush Terra",
                       "11. Dominio Fora Padrão (Paredão pra ir Secret)", "12. Domínio Fora Agg (Smoke Terra e Garagem)", "13. Peek Fora",
                       "14. Rush Secret", "15. Leo Drunky"],
            "meio": ["1. Rush Rampa B", "2. Exec B", "3. Dominio Rampa", "4. Peek Cat", "5. Rush Casinha", "6. Peek Casinha",
                     "7. Exec A Miolo", "8. Wrap A (Miolo + Terra)", "9. Exec Secret", "10. Peek Fora", "11. Rush Terra", "12. Tentar Subir Cat",
                     "13. Wrap A Drunky (Miolo + Cat)", "14. Wrap Rampa Drunky (Rádio + Cat)", "15. Fake A Descer Duto"],
            "fim": ["1. Exec B", "2. Split B", "3. Fake Exec B", "4. Wrap A Drunky (Miolo + Cat)", "5. Exec A Miolo",
                    "6. Wrap A (Miolo + Terra)", "7. Descer Duto", "8. Exec Secret", "9. Exec Terra"]
        },
        "ct": {
            "inicio": ["1. Anti-Rush Rampa", "2. Avanço Rampa", "3. Anti-Rush Duto", "4. Forte A", "5. Peek Porta", "6. Avanço Fora",
                       "7. Batida Fora", "8. Secret Rápido"],
            "meio": ["1. Avanço Rampa", "2. Givada Rampa", "3. Bait Rampa", "4. Forte B", "5. Forte A", "6. Batida Miolo Casinha",
                     "7. Batida Miolo Porta", "8. Forte Fora", "9. Batida Fora", "10. Double Secret", "11. Givada Fora", "12. Stack A", "13; Stack B"],
            "fim": ["1. Bait B", "2. Forte B", "3. Forte Rampa", "4. Forte A", "5. Um Duto", "6. Bait Casinha", "7. Double Terra",
                    "8. Retake A", "9. Forte Fora", "10. Off Angle Garagem", "11. Retake B", "12. Stack A", "13. Stack B"]
        }
    },
    "Anubis": {
        "tr": {
            "inicio": ["1. Anti Rush Fundo B", "2. Peek Fundo B", "3. Rush Fundo B", "4. Domínio Ponte", "5. Peek Ponte", "6. Domínio Agua",
                       "7. Peek Água", "8. Domínio Fundo A", "9. Peek Fundo A"
        ],
        "meio": [
            "1. Exec A (Smokes CT + Liga A)", 
            "2. Split A (Fundo A + Ponte)", 
            "3. Rush B (Fundo B + Caverna)", 
            "4. Fake B (Smokes Liga B)", 
            "5. Dominar Água (Controle Caverna)", 
            "6. Baitar Rotação (Fake A)", 
            "7. Redominar Ponte", 
            "8. Utilidade Anti-Player Pirâmide"
        ],
        "fim": [
            "1. Execução Caverna B", 
            "2. Split B (Fundo B + Liga B)", 
            "3. Contato Fundo A", 
            "4. Fake A (Smokes Ponte)", 
            "5. Wrap Água para B", 
            "6. 5-man Rush Fundo B"
        ]
        },
        "ct": {
            "inicio": [
            "1. Utilidade Ponte (Smoke/Molly)", 
            "2. Dois Água", 
            "3. Peek Fundo A", 
            "4. Rush Meio", 
            "5. Default (2 A / 3 B)"
        ],
            "meio": [
            "1. Retake A (Flash Liga A)", 
            "2. Stack Caverna", 
            "3. Bait Fundo B", 
            "4. Avanço Ponte", 
            "5. Utilidade Anti-Rush Água", 
            "6. AWP Fundo A"
        ],
            "fim": [
            "1. Retake B (Smokes Fundo B + Liga B)", 
            "2. Defesa Forte A (Crossfire Ponte)", 
            "3. Utilidade Pós-Plante (Molotov CT)", 
            "4. Off-Angles Pirâmide", 
            "5. Stack 4 A (Anti-Execução)"
            ]
        }
    },
    "Ancient": {
    "tr": {
        "inicio": [
            "1. Dominar Quadrado", 
            "2. Peek Meio", 
            "3. Avanço Fundo A", 
            "4. Pressão Rampa B", 
            "5. Default (Lurks Caverna/Quadrado)"
        ],
        "meio": [
            "1. Exec A (Smokes CT + Fundo A)", 
            "2. Split A (Quadrado + Fundo A)", 
            "3. Rush B (Caverna + Rampa)", 
            "4. Fake A (Smokes Quadrado)", 
            "5. Controle Total Meio", 
            "6. Baitar Rotação CT (Fake B)", 
            "7. Redominar Fundo A", 
            "8. Utilidade Anti-Player Caverna"
        ],
        "fim": [
            "1. Execução Rampa B", 
            "2. Split B (Caverna + Rampa)", 
            "3. Contato Fundo A", 
            "4. Fake B (Utilidade Caverna)", 
            "5. Wrap Quadrado para A", 
            "6. 5-man Rush Caverna"
        ]
    },
    "ct": {
        "inicio": [
            "1. Utilidade Quadrado (Molotov/Flash)", 
            "2. Dois Meio", 
            "3. Peek Fundo A", 
            "4. Rush Meio", 
            "5. Default (3 A / 2 B)"
        ],
        "meio": [
            "1. Retake A (Smokes Fundo A)", 
            "2. Stack Caverna", 
            "3. Bait Rampa B", 
            "4. Avanço Quadrado", 
            "5. Utilidade Anti-Rush Fundo A", 
            "6. Double AWP Meio"
        ],
        "fim": [
            "1. Retake B (Smokes Rampa + Caverna)", 
            "2. Defesa Forte A (Crossfire Quadrado)", 
            "3. Utilidade Pós-Plante (Molotov CT)", 
            "4. Off-Angles Fundo A", 
            "5. Stack 4 B (Anti-Execução)"
        ]
    }
    },
    "Train": {
    "tr": {
        "inicio": [
            "1. Dominar Bombeiro", 
            "2. Peek Meio", 
            "3. Avanço Fundo", 
            "4. Controle Casa Branca", 
            "5. Default (Lurks Túnel/Trilhos)"
        ],
        "meio": [
            "1. Exec A (Smokes CT + Escuro)", 
            "2. Split A (Bombeiro + Fundo)", 
            "3. Rush B (Baixo + Gaules)", 
            "4. Fake A (Smokes Meio)", 
            "5. Dominar Gaules (Controle Casa Branca)", 
            "6. Baitar Rotação (Fake B)", 
            "7. Redominar Bomb Antigo", 
            "8. Utilidade Anti-Player Trilhos"
        ],
        "fim": [
            "1. Execução Gaules", 
            "2. Split B (Baixo + Gaules)", 
            "3. Contato Bomb Antigo", 
            "4. Fake B (Smokes Túnel)", 
            "5. Wrap Meio para A", 
            "6. 5-man Rush Baixo"
        ]
    },
    "ct": {
        "inicio": [
            "1. Anti-Rush Bombeiro (Molotov)", 
            "2. Dois Casa Branca", 
            "3. Peek Gaules", 
            "4. Rush Meio", 
            "5. Default (2 A / 3 B)"
        ],
        "meio": [
            "1. Retake A (Flash Escuro)", 
            "2. Stack Gaules", 
            "3. Bait Túnel", 
            "4. Avanço Bomb Antigo", 
            "5. Utilidade Anti-Rush Fundo", 
            "6. AWP Meio"
        ],
        "fim": [
            "1. Retake B (Smokes Baixo + Gaules)", 
            "2. Defesa Forte A (Crossfire Bombeiro)", 
            "3. Utilidade Pós-Plante (Molotov CT)", 
            "4. Off-Angles Bomb Antigo", 
            "5. Stack 4 B (Anti-Execução)"
        ]
    }
    }
}



# Estratégias e resultados
def estrategia_resultado(estrategia_ct: str, estrategia_tr: str) -> str:
    if estrategia_ct == estrategia_tr:
        return random.choice(["ct", "tr"])
    elif (estrategia_ct == "1" and estrategia_tr == "3") or \
         (estrategia_ct == "2" and estrategia_tr == "4") or \
         (estrategia_ct == "3" and estrategia_tr == "1") or \
         (estrategia_ct == "4" and estrategia_tr == "2"):
        return "ct"
    else:
        return "tr"