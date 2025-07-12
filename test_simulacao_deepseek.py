# test_funcoes_simulacao_deepseek.py
import unittest
from unittest.mock import patch, MagicMock, call
from funcoes_simulacao_deepseek import (
    validar_time,
    escolher_estrategia,
    jogar_half,
    jogar_mapa,
    jogar_partida,
    ResultadoMapa,
    ResultadoPartida,
    times,
    calcular_over_medio,
    decidir_vencedor_round
)
from estrategias_deepseek import estrategia_resultado

# ==================== TESTES UNITÁRIOS ====================
times.extend(["Furia", "G2"])

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

class TestEstrategiaResultado(unittest.TestCase):
    def test_ct_vence(self):
        # Testa combinação onde CT deve vencer
        mapa = "Mirage"
        self.assertEqual(estrategia_resultado("1", "1", mapa), "ct")

    def test_tr_vence(self):
        # Testa combinação onde TR deve vencer
        mapa = "Mirage"
        self.assertEqual(estrategia_resultado("1", "2", mapa), "tr")

    def test_aleatorio(self):
        # Testa combinação não definida nas regras
        mapa = "Mirage"
        resultado = estrategia_resultado("4", "4", mapa)
        self.assertIn(resultado, ["ct", "tr"])

    def test_mapa_invalido(self):
        with self.assertRaises(ValueError):
            estrategia_resultado("1", "1", "MapaInexistente")

class TestDecidirVencedorRound(unittest.TestCase):
    @patch('funcoes_simulacao_deepseek.calcular_probabilidade_vitoria')
    def test_decide_vencedor(self, mock_probabilidade):
        # Configura probabilidade para CT vencer
        mock_probabilidade.return_value = 0.8  # 80% de chance de CT vencer
        
        # CT deve vencer na maioria dos casos
        resultados = [decidir_vencedor_round(80, 70, "ct", "1", "2") for _ in range(100)]
        ct_wins = resultados.count("ct")
        self.assertGreater(ct_wins, 55)  # Deve vencer pelo menos 70% das vezes
        
        # Configura probabilidade para TR vencer
        mock_probabilidade.return_value = 0.3  # 30% de chance de CT vencer (70% de TR)
        
        # TR deve vencer na maioria dos casos
        resultados = [decidir_vencedor_round(70, 80, "tr", "2", "1") for _ in range(100)]
        tr_wins = resultados.count("tr")
        self.assertGreater(tr_wins, 55)

class TestJogarHalf(unittest.TestCase):
    @patch('funcoes_simulacao_deepseek.escolher_estrategia')
    @patch('funcoes_simulacao_deepseek.calcular_over_medio')
    @patch('funcoes_simulacao_deepseek.decidir_vencedor_round')
    def test_half_normal(self, mock_decidir, mock_over, mock_estrategia):
        # Configura mocks
        mock_estrategia.side_effect = [0, 0] * 12  # 24 valores (2 por round)
        mock_over.side_effect = [85.0, 80.0]  # Over para CT e TR
        mock_decidir.side_effect = ["ct"] * 12  # CT vence todos os rounds
        
        ct, tr = jogar_half("Furia", "G2", "Dust2", "auto")
        
        self.assertEqual(ct, 12)
        self.assertEqual(tr, 0)
        
        # Verifica se calcular_over_medio foi chamado corretamente
        mock_over.assert_any_call("Furia")
        mock_over.assert_any_call("G2")
        
        # Verifica se decidir_vencedor_round foi chamado 12 vezes
        self.assertEqual(mock_decidir.call_count, 12)

    @patch('funcoes_simulacao_deepseek.escolher_estrategia')
    @patch('funcoes_simulacao_deepseek.calcular_over_medio')
    @patch('funcoes_simulacao_deepseek.decidir_vencedor_round')
    def test_half_misto(self, mock_decidir, mock_over, mock_estrategia):
        # Configura vitórias alternadas
        mock_estrategia.side_effect = [0, 0] * 12
        mock_over.side_effect = [85.0, 80.0]
        mock_decidir.side_effect = ["ct", "tr"] * 6  # Alterna vitórias
        
        ct, tr = jogar_half("Furia", "G2", "Dust2", "auto")
        
        self.assertEqual(ct, 6)
        self.assertEqual(tr, 6)

class TestJogarMapa(unittest.TestCase):
    @patch('funcoes_simulacao_deepseek.jogar_half')
    def test_mapa_completo(self, mock_half):
        mock_half.side_effect = [(10, 2), (5, 3)]  # Primeiro half: 10-2, segundo: 5-3
        
        resultado = jogar_mapa("Furia", "G2", "Dust2", "auto")
        self.assertEqual(resultado.placar_time1, 13)  # 10 + 3 = 13
        self.assertEqual(resultado.placar_time2, 7)    # 2 + 5 = 7

    @patch('funcoes_simulacao_deepseek.jogar_half')
    def test_vitoria_rapida(self, mock_half):
        mock_half.return_value = (13, 0)  # Vitória no primeiro half
        resultado = jogar_mapa("Furia", "G2", "Dust2", "auto")
        self.assertEqual(resultado.placar_time1, 13)
        self.assertEqual(resultado.placar_time2, 0)

    @patch('funcoes_simulacao_deepseek.jogar_half')
    def test_overtime(self, mock_half):
        # Primeiro half: empate 10-10
        # Segundo half: empate 3-3 (total 13-13)
        # Overtime: Furia vence 4-2
        mock_half.side_effect = [
            (10, 10),   # Primeiro half
            (3, 3),      # Segundo half (continuação)
            (2, 1),      # Primeira parte do overtime (CT)
            (1, 1)       # Segunda parte do overtime (TR)
        ]
        
        resultado = jogar_mapa("Furia", "G2", "Dust2", "auto")
        self.assertEqual(resultado.placar_time1, 16)  # 10 + 3 + 2 + 1 = 16
        self.assertEqual(resultado.placar_time2, 15)  # 10 + 3 + 1 + 1 = 15

class TestJogarPartida(unittest.TestCase):
    @patch('funcoes_simulacao_deepseek.vetar_e_escolher_mapas')
    @patch('funcoes_simulacao_deepseek.jogar_mapa')
    @patch('funcoes_simulacao_deepseek.calcular_over_medio')
    def test_partida_valida(self, mock_over, mock_mapa, mock_vetar):
        # 1. Garantir que os times existam
        times.extend(["Furia", "G2"])
        
        # 2. Configurar mocks
        mock_vetar.return_value = ["Dust2", "Inferno", "Mirage"]
        mock_over.return_value = 80.0  # Valor fixo para over
        
        # 3. Criar objetos ResultadoMapa completos
        mock_mapa.side_effect = [
            ResultadoMapa(
                mapa="Dust2",
                time_ct="Furia",
                time_tr="G2",
                placar_time1=13,
                placar_time2=7
            ),
            ResultadoMapa(
                mapa="Inferno",
                time_ct="Furia",
                time_tr="G2",
                placar_time1=10,
                placar_time2=13
            ),
            ResultadoMapa(
                mapa="Mirage",
                time_ct="Furia",
                time_tr="G2",
                placar_time1=13,
                placar_time2=1
            )
        ]
        
        # 4. Executar teste
        resultado = jogar_partida(modo='auto', time1="Furia", time2="G2")
        
        # 5. Verificações
        self.assertIsInstance(resultado, ResultadoPartida)
        self.assertEqual(len(resultado.mapas), 3)
        self.assertEqual(resultado.vencedor, "Furia")
        
        # 6. Limpeza
        times.remove("Furia")
        times.remove("G2")

    @patch('funcoes_simulacao_deepseek.vetar_e_escolher_mapas', return_value=[])
    @patch('funcoes_simulacao_deepseek.calcular_over_medio')
    def test_sem_mapas_validos(self, mock_over, mock_vetar):
        mock_over.return_value = 80.0
        times.extend(["Furia", "G2"])
        resultado = jogar_partida(modo='auto', time1="Furia", time2="G2")
        self.assertIsNone(resultado)
        times.remove("Furia")
        times.remove("G2")

# ==================== TESTES DE INTEGRAÇÃO ====================

class TestIntegracao(unittest.TestCase):
    @patch('funcoes_simulacao_deepseek.vetar_e_escolher_mapas')
    @patch('funcoes_simulacao_deepseek.jogar_mapa')
    @patch('funcoes_simulacao_deepseek.calcular_over_medio')
    def test_fluxo_completo(self, mock_over, mock_mapa, mock_vetar):
        # 1. Garantir que os times existam
        times.extend(["Furia", "G2"])
        
        # 2. Configurar mocks
        mock_vetar.return_value = ["Dust2", "Inferno", "Mirage"]
        mock_over.return_value = 80.0  # Valor fixo para over
        
        # 3. Criar objetos ResultadoMapa completos
        mock_mapa.side_effect = [
            ResultadoMapa(
                mapa="Dust2",
                time_ct="Furia",
                time_tr="G2",
                placar_time1=13,
                placar_time2=7
            ),
            ResultadoMapa(
                mapa="Inferno",
                time_ct="Furia",
                time_tr="G2",
                placar_time1=10,
                placar_time2=13
            ),
            ResultadoMapa(
                mapa="Mirage",
                time_ct="Furia",
                time_tr="G2",
                placar_time1=13,
                placar_time2=1
            )
        ]

        # 4. Executar teste
        resultado = jogar_partida(modo='auto', time1="Furia", time2="G2")
        
        # 5. Verificações
        self.assertIsNotNone(resultado)
        self.assertEqual(len(resultado.mapas), 3)
        self.assertEqual(resultado.vencedor, "Furia")
        
        # 6. Limpeza
        times.remove("Furia")
        times.remove("G2")
        
# ==================== EXECUÇÃO DOS TESTES ====================

if __name__ == '__main__':
    unittest.main(verbosity=2)