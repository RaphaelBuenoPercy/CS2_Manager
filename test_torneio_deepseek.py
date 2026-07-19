import unittest
from unittest.mock import patch
from funcoes_torneio_deepseek import *


class TestTorneio(unittest.TestCase):
    def setUp(self):
        self.times = ["FURIA", "Liquid", "Vitality", "NaVi", "G2", "Heroic"]

    @patch("builtins.input", side_effect=["3", "2"])
    def test_validar_num_grupos(self, mock_input):
        result = validar_num_grupos(self.times, 2)
        self.assertEqual(result, 2)

    @patch("builtins.input", side_effect=["1 3 6"])
    def test_selecionar_times(self, mock_input):
        result = selecionar_times(self.times, 3)
        self.assertEqual(result, ["FURIA", "Vitality", "Heroic"])

    def test_sortear_grupos(self):
        grupos = sortear_grupos(self.times, 2)
        self.assertEqual(len(grupos), 2)
        self.assertEqual(sum(len(g) for g in grupos), 6)

    @patch("builtins.input", side_effect=["abc", "5"])
    def test_validar_input_numerico(self, mock_input):
        result = validar_input_numerico("Teste: ", min_val=1, max_val=10)
        self.assertEqual(result, 5)

    def test_fase_mata_mata_invalida(self):
        with self.assertRaises(ValueError):
            fase_mata_mata(self.times, [])

    @patch("funcoes_torneio_deepseek.simular_partida_auto")
    @patch("funcoes_torneio_deepseek.obter_opcao_numerica")
    @patch("builtins.input")
    def test_fase_mata_mata_sem_time_usuario_e_100_por_cento_automatica(
        self, mock_input, mock_opcao, mock_simular_auto
    ):
        """Sem time_usuario, nenhuma partida deve pedir interação: tudo é auto-simulado."""
        times4 = ["A", "B", "C", "D"]

        def fake_simular(time1, time2, fase):
            resultado = ResultadoPartida(partida_id=1, mapas=[])
            return time1, time2, resultado

        mock_simular_auto.side_effect = fake_simular

        vencedores, resultados = fase_mata_mata(times4, [])

        # Nenhuma chamada de input ou de menu de escolha de modo de partida
        mock_input.assert_not_called()
        mock_opcao.assert_not_called()
        # Semifinal (2 jogos) + Final (1 jogo) = 3 partidas simuladas automaticamente
        self.assertEqual(mock_simular_auto.call_count, 3)
        self.assertEqual(len(resultados), 3)

    @patch("funcoes_torneio_deepseek.simular_partida_auto")
    @patch("funcoes_torneio_deepseek.jogar_partida")
    @patch("funcoes_torneio_deepseek.obter_opcao_numerica")
    def test_fase_mata_mata_so_pergunta_pelas_partidas_do_usuario(
        self, mock_opcao, mock_jogar_partida, mock_simular_auto
    ):
        """Com time_usuario definido, só as partidas do jogador pedem escolha de modo;
        partidas de terceiros continuam 100% automáticas, sem chance de interferência.
        """
        times4 = ["MeuTime", "B", "C", "D"]

        # Modo escolhido pelo usuário nas suas próprias partidas: "Partida Rápida"
        mock_opcao.return_value = 1

        def fake_jogar_partida(modo, time1, time2, fase_torneio):
            resultado = ResultadoPartida(partida_id=1, mapas=[])
            resultado.vencedor = time1
            resultado.perdedor = time2
            return resultado

        def fake_simular_auto(time1, time2, fase):
            resultado = ResultadoPartida(partida_id=2, mapas=[])
            return time1, time2, resultado

        mock_jogar_partida.side_effect = fake_jogar_partida
        mock_simular_auto.side_effect = fake_simular_auto

        vencedores, resultados = fase_mata_mata(times4, [], time_usuario="MeuTime")

        # jogar_partida (interativo) só é chamado nas partidas em que "MeuTime" participa
        for chamada in mock_jogar_partida.call_args_list:
            self.assertIn("MeuTime", (chamada.kwargs["time1"], chamada.kwargs["time2"]))

        # obter_opcao_numerica só deve ser chamado uma vez por partida do usuário
        self.assertEqual(mock_opcao.call_count, mock_jogar_partida.call_count)

        # Partidas de terceiros nunca passam por jogar_partida (interativo)
        for chamada in mock_simular_auto.call_args_list:
            self.assertNotIn("MeuTime", chamada.args[:2])


if __name__ == "__main__":
    unittest.main()
