# test_funcoes_simulacao_deepseek.py
import unittest
from unittest.mock import patch, MagicMock
from funcoes_simulacao_deepseek import (
    validar_time,
    escolher_estrategia,
    jogar_half,
    jogar_mapa,
    jogar_partida,
    ResultadoMapa,
    ResultadoPartida,
    times,
    estrategias_por_mapa
)

# ==================== TESTES UNITÁRIOS ====================
times.extend(["Alpha", "Beta"])

class TestValidarTime(unittest.TestCase):
    def test_time_valido(self):
        times.append("TimeTeste")
        self.assertEqual(validar_time("TimeTeste"), "TimeTeste")
        times.remove("TimeTeste")

    def test_time_invalido(self):
        with self.assertRaises(ValueError):
            validar_time("TimeInexistente")

class TestEscolherEstrategia(unittest.TestCase):
    @patch('builtins.input', return_value='2')
    def test_modo_manual(self, mock_input):
        estrategias = ["Rush", "Defesa"]
        self.assertEqual(escolher_estrategia("Jogador", estrategias, 'manual'), 1)

    def test_modo_auto(self):
        estrategias = ["Rush", "Defesa"]
        with patch('random.randint', return_value=0):
            self.assertEqual(escolher_estrategia("Bot", estrategias, 'auto'), 0)

class TestJogarHalf(unittest.TestCase):
    @patch('funcoes_simulacao_deepseek.escolher_estrategia')
    @patch('funcoes_simulacao_deepseek.estrategia_resultado')
    @patch.dict('estrategias.estrategias_por_mapa', 
                {'Dust2': {'ct': ['Estratégia1', 'Estratégia2'], 
                          'tr': ['Estratégia3', 'Estratégia4']}})
    def test_half_normal(self, mock_resultado, mock_estrategia):
        # Configuração para 12 rounds (24 chamadas: 2 por round)
        mock_estrategia.side_effect = [0, 0] * 12  # 24 valores (2 por round)
        mock_resultado.return_value = "ct"  # CT vence todos os rounds
        
        ct, tr = jogar_half("Alpha", "Beta", "Dust2", "auto")
        
        self.assertEqual(ct, 12)  # CT venceu todos os 12 rounds
        self.assertEqual(tr, 0)

    def test_mapa_invalido(self):
        with self.assertRaises(ValueError):
            jogar_half("Alpha", "Beta", "mapa_falso", "auto")

class TestJogarMapa(unittest.TestCase):
    @patch('funcoes_simulacao_deepseek.jogar_half')
    def test_mapa_completo(self, mock_half):
        mock_half.side_effect = [(10, 2), (5, 3)]
        
        resultado = jogar_mapa("Alpha", "Beta", "Dust2", "auto")
        self.assertEqual(resultado.placar_time1, 13)
        self.assertEqual(resultado.placar_time2, 7)

    @patch('funcoes_simulacao_deepseek.jogar_half')
    def test_vitoria_rapida(self, mock_half):
        mock_half.return_value = (13, 0)
        resultado = jogar_mapa("Alpha", "Beta", "Dust2", "auto")
        self.assertEqual(resultado.placar_time2, 0)

class TestJogarPartida(unittest.TestCase):
    @patch('funcoes_simulacao_deepseek.vetar_e_escolher_mapas')
    @patch('funcoes_simulacao_deepseek.jogar_mapa')
    def test_partida_valida(self, mock_mapa, mock_vetar):
        # Configuração para 3 mapas (melhor de 3)
        mock_vetar.return_value = ["Dust2", "Inferno", "Mirage"]
        
        # Simula resultados sequenciais dos mapas:
        # - Alpha vence o primeiro
        # - Beta vence o segundo
        # - Alpha vence o terceiro
        mock_mapa.side_effect = [
            ResultadoMapa(
                mapa="Dust2",
                time_ct="Alpha",
                time_tr="Beta",
                placar_time1=13,
                placar_time2= 7
            ),
            ResultadoMapa(
                mapa="Inferno",
                time_ct="Alpha",
                time_tr="Beta",
                placar_time1=10,
                placar_time2=13
            ),
            ResultadoMapa(
                mapa="Mirage",
                time_ct="Alpha",
                time_tr="Beta",
                placar_time1=13,
                placar_time2=1
            )
        ]
        
        # Executa a partida
        resultado = jogar_partida(modo='auto', time1="Alpha", time2="Beta")
        
        # Verificações
        self.assertIsInstance(resultado, ResultadoPartida)
        self.assertEqual(len(resultado.mapas), 3)  # Todos os mapas executados
        self.assertEqual(resultado.vencedor, "Alpha")
        
        # Verifica a contagem de vitórias
        vitorias_alpha = sum(1 for m in resultado.mapas if m.placar_time1 > m.placar_time2)
        vitorias_beta = sum(1 for m in resultado.mapas if m.placar_time2 > m.placar_time1)
        self.assertEqual(vitorias_alpha, 2)
        self.assertEqual(vitorias_beta, 1)

    @patch('funcoes_simulacao_deepseek.vetar_e_escolher_mapas', return_value=[])
    def test_sem_mapas_validos(self, mock_vetar):
        resultado = jogar_partida(modo='auto', time1="Alpha", time2="Beta")
        self.assertIsNone(resultado)

# ==================== TESTES DE INTEGRAÇÃO ====================

class TestIntegracao(unittest.TestCase):
    @patch('funcoes_simulacao_deepseek.vetar_e_escolher_mapas')
    @patch('funcoes_simulacao_deepseek.jogar_mapa')
    @patch('funcoes_simulacao_deepseek.estrategia_resultado')
    def test_fluxo_completo(self, mock_resultado, mock_mapa, mock_vetar):
        # Configurar mocks
        mock_vetar.return_value = ["Dust2", "Inferno", "Mirage"]
        mock_resultado.side_effect = ["ct", "tr"] * 6  # Padrão de resultados alternados
        
        # Configurar resultados sequenciais para cada mapa
        mock_mapa.side_effect = [
            ResultadoMapa(
                mapa="Dust2",
                time_ct="Alpha",
                time_tr="Beta",
                placar_time1=13,
                placar_time2=7
            ),
            ResultadoMapa(
                mapa="Inferno",
                time_ct="Alpha",
                time_tr="Beta",
                placar_time1=10,
                placar_time2=13
            ),
            ResultadoMapa(
                mapa="Mirage",
                time_ct="Alpha",
                time_tr="Beta",
                placar_time1=13,
                placar_time2=1
            )
        ]

        # Executar teste
        times.extend(["Alpha", "Beta"])
        resultado = jogar_partida(modo='auto', time1="Alpha", time2="Beta")
        
        # Verificações
        self.assertIsNotNone(resultado)
        self.assertEqual(len(resultado.mapas), 3)  # Para ao atingir 2 vitórias
        self.assertEqual(resultado.vencedor, "Alpha")
        
        # Limpeza
        times.remove("Alpha")
        times.remove("Beta")

# ==================== EXECUÇÃO DOS TESTES ====================

if __name__ == '__main__':
    unittest.main(verbosity=2)