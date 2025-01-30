import unittest
from unittest.mock import patch
from funcoes_torneio_deepseek import *

class TestTorneio(unittest.TestCase):
    def setUp(self):
        self.times = ["FURIA", "Liquid", "Vitality", "NaVi", "G2", "Heroic"]

    @patch('builtins.input', side_effect=['3', '2'])
    def test_validar_num_grupos(self, mock_input):
        result = validar_num_grupos(self.times, 3)
        self.assertEqual(result, 2)

    @patch('builtins.input', side_effect=['1 3 5'])
    def test_selecionar_times(self, mock_input):
        result = selecionar_times(self.times, 3)
        self.assertEqual(result, ["FURIA", "Vitality", "Heroic"])

    def test_sortear_grupos(self):
        grupos = sortear_grupos(self.times, 2)
        self.assertEqual(len(grupos), 2)
        self.assertEqual(sum(len(g) for g in grupos), 6)

    @patch('builtins.input', side_effect=['abc', '5'])
    def test_validar_input_numerico(self, mock_input):
        result = validar_input_numerico("Teste: ", min_val=1, max_val=10)
        self.assertEqual(result, 5)

    def test_fase_mata_mata_invalida(self):
        with self.assertRaises(ValueError):
            fase_mata_mata(self.times, [])

if __name__ == '__main__':
    unittest.main()