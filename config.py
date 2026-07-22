# config.py
"""Configurações centrais do simulador.

Antes, "times.csv" e "jogadores.csv" apareciam hardcoded e duplicados em
vários arquivos diferentes (funcoes_prejogo_deepseek.py,
funcoes_simulacao_deepseek.py, Menu_Helper.py, gerador_kills_deaths.py...).
Qualquer mudança de nome ou de local do arquivo exigia caçar cada
ocorrência manualmente — e era fácil esquecer uma (foi mais ou menos assim
que o bug do cabeçalho de times.csv passou despercebido por um tempo).

Agora todo módulo que precisa desses caminhos importa daqui.
"""

TIMES_CSV = "times.csv"
JOGADORES_CSV = "jogadores.csv"
