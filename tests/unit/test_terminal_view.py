"""
Testes Unitários para a Terminal View
"""
import unittest
import io
import sys
import os
from unittest.mock import patch, MagicMock

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.views.terminal_view import TerminalView
from src.models.analisador import ResultadoAnalise

class TestTerminalView(unittest.TestCase):
    """Testes para o componente TerminalView"""
    
    def setUp(self):
        """Configuração antes de cada teste"""
        self.view = TerminalView()
        
    def test_init_terminal_view(self):
        """Testa inicialização da TerminalView"""
        self.assertEqual(self.view.largura_tela, 120)
        self.assertIn("SWAIF-CONFA", self.view.titulo_sistema)
        
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_exibir_cabecalho(self, mock_stdout):
        """Testa exibição do cabeçalho"""
        self.view.exibir_cabecalho()
        output = mock_stdout.getvalue()
        
        self.assertIn("SWAIF-CONFA", output)
        self.assertIn("=", output)
        
    @patch('builtins.input', return_value='1')
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_exibir_menu_principal(self, mock_stdout, mock_input):
        """Testa exibição do menu principal"""
        with patch.object(self.view, 'limpar_tela'):
            opcao = self.view.exibir_menu_principal()
        
        output = mock_stdout.getvalue()
        self.assertIn("MENU PRINCIPAL", output)
        self.assertIn("1. Executar Conciliação", output)
        self.assertEqual(opcao, '1')
        
    @patch('builtins.input', return_value='072025')
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_solicitar_mes_ano(self, mock_stdout, mock_input):
        """Testa solicitação de mês e ano"""
        mes_ano = self.view.solicitar_mes_ano()
        
        output = mock_stdout.getvalue()
        self.assertIn("mês e ano", output)
        self.assertIn("072025", output)
        self.assertEqual(mes_ano, '072025')
        
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_exibir_resultados_conciliacao(self, mock_stdout):
        """Testa exibição de resultados de conciliação"""
        # Cria resultados de teste
        resultados = [
            ResultadoAnalise(
                par_fontes=('faturamento_c6', 'faturamento_gds'),
                total_fonte_1=1000.0,
                total_fonte_2=1100.0,
                registros_fonte_1=10,
                registros_fonte_2=11,
                diferenca=100.0,
                percentual_diferenca=10.0
            ),
            ResultadoAnalise(
                par_fontes=('pagamento_c6', 'pagamento_gds'),
                total_fonte_1=950.0,
                total_fonte_2=980.0,
                registros_fonte_1=8,
                registros_fonte_2=9,
                diferenca=30.0,
                percentual_diferenca=3.16
            )
        ]
        
        with patch.object(self.view, 'limpar_tela'):
            self.view.exibir_resultados_conciliacao(resultados, '072025')
        
        output = mock_stdout.getvalue()
        self.assertIn("RESULTADOS DA CONCILIAÇÃO", output)
        self.assertIn("faturamento_c6", output)
        self.assertIn("faturamento_gds", output)
        self.assertIn("1.000,00", output)  # Formato monetário
        self.assertIn("10,0%", output)     # Percentual
        
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_exibir_resultados_vazios(self, mock_stdout):
        """Testa exibição com resultados vazios"""
        resultados = []
        
        with patch.object(self.view, 'limpar_tela'):
            self.view.exibir_resultados_conciliacao(resultados, '072025')
        
        output = mock_stdout.getvalue()
        self.assertIn("Nenhum resultado", output)
        
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_exibir_resumo_dados(self, mock_stdout):
        """Testa exibição de resumo de dados"""
        resumo = {
            'faturamento_c6': {
                'registros': 10,
                'colunas': ['data_venda', 'valor_venda', 'cliente']
            },
            'faturamento_gds': {
                'registros': 15,
                'colunas': ['data', 'valor', 'cliente']
            },
            'pagamento_c6': {
                'registros': 8,
                'colunas': ['data_recebivel', 'valor_recebivel']
            }
        }
        
        with patch.object(self.view, 'limpar_tela'):
            self.view.exibir_resumo_dados(resumo, '072025')
        
        output = mock_stdout.getvalue()
        self.assertIn("RESUMO DOS DADOS", output)
        self.assertIn("faturamento_c6", output)
        self.assertIn("10 registros", output)
        self.assertIn("3 colunas", output)
        
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_exibir_detalhes_fonte_com_erro(self, mock_stdout):
        """Testa exibição de detalhes com erro"""
        detalhes = {
            'erro': 'Fonte não encontrada'
        }
        
        with patch.object(self.view, 'limpar_tela'), \
             patch('builtins.input', return_value=''):
            self.view.exibir_detalhes_fonte(detalhes, 'teste_fonte', '072025')
        
        output = mock_stdout.getvalue()
        self.assertIn("❌", output)
        self.assertIn("Fonte não encontrada", output)
        
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_exibir_detalhes_fonte_completo(self, mock_stdout):
        """Testa exibição completa de detalhes da fonte"""
        detalhes = {
            'registros': 25,
            'colunas': ['data_venda', 'valor_venda', 'cliente'],
            'total_principal': 5500.75,
            'tipo_total': 'Valor Faturado',
            'estatisticas': {
                'valor_venda': {
                    'total': 5500.75,
                    'media': 220.03,
                    'minimo': 50.00,
                    'maximo': 800.00
                }
            },
            'primeiros_registros': [
                {'data_venda': '01/07/2025', 'valor_venda': 100.0, 'cliente': 'Cliente A'},
                {'data_venda': '02/07/2025', 'valor_venda': 200.0, 'cliente': 'Cliente B'}
            ]
        }
        
        with patch.object(self.view, 'limpar_tela'), \
             patch('builtins.input', return_value=''):
            self.view.exibir_detalhes_fonte(detalhes, 'faturamento_c6', '072025')
        
        output = mock_stdout.getvalue()
        self.assertIn("DETALHES DA FONTE", output)
        self.assertIn("FATURAMENTO_C6", output)
        self.assertIn("25", output)  # Total de registros
        self.assertIn("💰", output)  # Ícone do total principal
        self.assertIn("VALOR FATURADO", output)
        self.assertIn("5.500,75", output)  # Total principal formatado
        self.assertIn("ESTATÍSTICAS", output)
        self.assertIn("PRIMEIROS REGISTROS", output)
        
    @patch('builtins.input', return_value='2')
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_solicitar_fonte_valida(self, mock_stdout, mock_input):
        """Testa solicitação de fonte válida"""
        fonte = self.view.solicitar_fonte()
        
        output = mock_stdout.getvalue()
        self.assertIn("Fontes disponíveis", output)
        self.assertIn("faturamento_c6", output)
        self.assertEqual(fonte, 'faturamento_gds')  # Opção 2
        
    @patch('builtins.input', side_effect=['10', '1'])  # Primeira entrada inválida, segunda válida
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_solicitar_fonte_invalida(self, mock_stdout, mock_input):
        """Testa solicitação de fonte com entrada inválida"""
        fonte = self.view.solicitar_fonte()
        
        output = mock_stdout.getvalue()
        self.assertIn("Opção inválida", output)
        self.assertEqual(fonte, 'faturamento_c6')  # Opção 1 (segunda tentativa)
        
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_exibir_erro(self, mock_stdout):
        """Testa exibição de erro"""
        with patch('builtins.input', return_value=''):
            self.view.exibir_erro("Teste de erro")
        
        output = mock_stdout.getvalue()
        self.assertIn("❌ ERRO", output)
        self.assertIn("Teste de erro", output)
        
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_exibir_processando(self, mock_stdout):
        """Testa exibição de processamento"""
        self.view.exibir_processando("Carregando dados...")
        
        output = mock_stdout.getvalue()
        self.assertIn("⏳", output)
        self.assertIn("Carregando dados", output)
        
    def test_formatar_mes_ano(self):
        """Testa formatação de mês/ano"""
        test_cases = [
            ('072025', 'Julho/2025'),
            ('012024', 'Janeiro/2024'),
            ('122023', 'Dezembro/2023'),
            ('042026', 'Abril/2026')
        ]
        
        for input_mes, expected in test_cases:
            with self.subTest(input_mes=input_mes):
                resultado = self.view._formatar_mes_ano(input_mes)
                self.assertEqual(resultado, expected)
                
    def test_formatar_mes_ano_invalido(self):
        """Testa formatação com mês inválido"""
        resultado = self.view._formatar_mes_ano('132025')  # Mês 13 inválido
        self.assertIn('13/2025', resultado)  # Deve retornar o valor original

if __name__ == '__main__':
    unittest.main()
