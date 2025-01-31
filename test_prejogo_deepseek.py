# test_prejogo_deepseek.py
import unittest
from unittest.mock import patch, mock_open, MagicMock
from funcoes_prejogo_deepseek import *

class TestPreJogo(unittest.TestCase):
    def setUp(self):
        # Resetar estado global entre testes
        times.clear()
        global estrategias_por_mapa
        self.original_mapas = estrategias_por_mapa.copy()

    def tearDown(self):
        # Restaurar mapas originais
        global estrategias_por_mapa
        estrategias_por_mapa = self.original_mapas.copy()

    # Testes para adicionar_time()
    def test_adicionar_time_valido(self):
        adicionar_time("FURIA")
        self.assertIn("FURIA", times)
        self.assertEqual(len(times), 1)

    def test_adicionar_time_duplicado(self):
        adicionar_time("MIBR")
        with self.assertRaisesRegex(ValueError, "Time 'MIBR' já está registrado"):
            adicionar_time("MIBR")

    def test_adicionar_time_vazio(self):
        with self.assertRaisesRegex(ValueError, "Nome do time não pode ser vazio"):
            adicionar_time("")

    # Testes para carregar_times_csv()
    @patch('builtins.open', new_callable=mock_open, read_data="FURIA\nMIBR\nLiquid")
    def test_carregar_csv_valido(self, mock_file):
        carregar_times_csv("dummy.csv")
        self.assertListEqual(times, ["FURIA", "MIBR", "Liquid"])

    def test_carregar_csv_inexistente(self):
        with self.assertRaises(FileNotFoundError):
            carregar_times_csv("arquivo_inexistente.csv")

    # Testes para listar_times()
    def test_listar_times_vazio(self):
        with patch('builtins.print') as mocked_print:
            listar_times()
            mocked_print.assert_called_with("Nenhum time registrado\n")

    def test_listar_times_preenchido(self):
        # Adiciona times à lista global
        times.extend(["Furia", "Mibr"])
        
        # Mock de print para verificar a saída
        with patch('builtins.print') as mocked_print:
            listar_times()  # Chama a função para listar os times

            # Verifica se os times foram listados com o número correto
            mocked_print.assert_any_call("  1. Furia")  # Verifica se "1. Furia" foi impresso
            mocked_print.assert_any_call("  2. Mibr")   # Verifica se "2. Mibr" foi impresso
            mocked_print.assert_any_call("Total: 2 times\n")  # Verifica se o total de times foi impresso corretamente

    # Testes para selecionar_mapa()
    @patch('builtins.input', side_effect=['2'])
    def test_selecionar_mapa_valido(self, mock_input):
        mapas = ["Inferno", "Mirage", "Dust2"]
        resultado = selecionar_mapa("Time A", mapas)
        self.assertEqual(resultado, "Mirage")
        self.assertListEqual(mapas, ["Inferno", "Dust2"])

    @patch('builtins.input', side_effect=['5', '1'])
    def test_selecionar_mapa_invalido(self, mock_input):
        mapas = ["Inferno", "Mirage"]
        resultado = selecionar_mapa("Time B", mapas)
        self.assertEqual(resultado, "Inferno")

    # Teste para vetar_e_escolher_mapas()
    @patch('builtins.input', side_effect=['1','1','1','1','1','1'])
    def test_veto_completo(self, mock_input):
        # Configurar mapas mockados
        global estrategias_por_mapa
        estrategias_por_mapa = {f"Mapa{i}": {} for i in range(1,8)}
        
        resultado = vetar_e_escolher_mapas("Time A", "Time B")
        self.assertEqual(len(resultado), 3)
        self.assertEqual(resultado[2], "Train")

if __name__ == '__main__':
    unittest.main()