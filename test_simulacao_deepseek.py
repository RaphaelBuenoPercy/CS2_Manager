# test_funcoes_simulacao.py
import unittest
from unittest.mock import patch, MagicMock
from funcoes_simulacao_deepseek import *
from funcoes_prejogo_deepseek import times

class TestSimulacao(unittest.TestCase):
    def setUp(self):
        # Resetar estados globais entre os testes
        times.clear()
        times.extend(["FURIA", "Liquid", "NAVI", "Vitality"])
        ContadorPartidas._id = 1
        self.resultado_mapas_mock = [
            ResultadoMapa(
                mapa="Inferno",
                time_ct="FURIA",
                time_tr="Liquid",
                placar_ct=16,
                placar_tr=14,
                rounds_extra=6
            )
        ]

    # ==================== TESTES OVERTIMEMANAGER ====================
    def test_overtime_manager_alternancia_lados(self):
        manager = OvertimeManager("FURIA", "Liquid")
        initial_ct = manager.time_ct
        
        # Simular 3 rounds
        for _ in range(3):
            manager.verificar_mudanca_half()
        
        self.assertNotEqual(initial_ct, manager.time_ct)

    def test_atualizacao_meta_overtime(self):
        manager = OvertimeManager("FURIA", "Liquid")
        manager.atualizar_meta(15, 15)
        self.assertEqual(manager.meta, 20)
        self.assertEqual(manager.rounds_por_half, 6)

    # ==================== TESTES ESCOLHA ESTRATÉGIA ====================
    @patch('builtins.input', side_effect=['2'])
    def test_escolha_estrategia_manual(self, mock_input):
        estrategias = ["Rush B", "Defesa A"]
        escolha = escolher_estrategia("Jogador", estrategias, 'manual')
        self.assertEqual(escolha, 1)

    def test_escolha_estrategia_auto(self):
        estrategias = ["Rush B", "Defesa A"]
        escolha = escolher_estrategia("Bot", estrategias, 'auto')
        self.assertTrue(0 <= escolha < len(estrategias))

    # ==================== TESTES JOGAR_HALF ====================
    @patch('funcoes_simulacao_deepseek.escolher_estrategia')
    def test_jogar_half_auto(self, mock_escolha):
        mock_escolha.side_effect = [0, 0]  # Ambos escolhem primeira estratégia
        ct, tr = jogar_half("FURIA", "Liquid", 0, 0, "Inferno", 'auto')
        self.assertTrue(ct >= 16 or tr >= 16)

    # ==================== TESTES JOGAR_MAPA ====================
    @patch('funcoes_simulacao_deepseek.jogar_half')
    def test_jogar_mapa_com_overtime(self, mock_half):
        # Configurar mock para simular overtime
        mock_half.side_effect = [
            (12, 12),   # Primeiro half
            (12, 12),   # Segundo half
            (16, 14)    # Overtime
        ]
        
        resultado = jogar_mapa("FURIA", "Liquid", "Inferno", 'auto')
        self.assertEqual(resultado.placar_ct, 16)
        self.assertEqual(resultado.placar_tr, 14)
        self.assertGreater(resultado.rounds_extra, 0)

    # ==================== TESTES JOGAR_PARTIDA ====================
    @patch('funcoes_simulacao_deepseek.vetar_e_escolher_mapas')
    @patch('funcoes_simulacao_deepseek.jogar_mapa')
    def test_jogar_partida_auto(self, mock_mapa, mock_veto):
        # Configurar mocks
        mock_veto.return_value = ["Inferno", "Mirage"]
        mock_mapa.return_value = self.resultado_mapas_mock[0]
        
        resultado = jogar_partida(modo='auto', time1="FURIA", time2="Liquid")
        
        self.assertEqual(resultado.vencedor, "FURIA")
        self.assertEqual(resultado.partida_id, 1)
        self.assertEqual(len(resultado.mapas), 1)

    @patch('funcoes_simulacao_deepseek.vetar_e_escolher_mapas')
    def test_jogar_partida_time_invalido(self, mock_veto):
        mock_veto.return_value = ["Inferno"]
        resultado = jogar_partida(modo='auto', time1="INVALIDO", time2="Liquid")
        self.assertIsNone(resultado)

if __name__ == '__main__':
    unittest.main()