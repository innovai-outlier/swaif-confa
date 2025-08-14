"""
Testes Unitários para o Controller
"""
import os
import shutil
import sys
import tempfile
import unittest

import pandas as pd

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.controllers.conciliacao_controller import ConciliacaoController


class TestConciliacaoController(unittest.TestCase):
    """Testes para o componente ConciliacaoController"""
    
    def setUp(self):
        """Configuração antes de cada teste"""
        self.temp_dir = tempfile.mkdtemp()
        self.controller = ConciliacaoController(self.temp_dir)
        
    def tearDown(self):
        """Limpeza após cada teste"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
        
    def test_init_controller(self):
        """Testa inicialização do Controller"""
        self.assertIsNotNone(self.controller.data_loader)
        self.assertIsNotNone(self.controller.analisador)
        self.assertIsNotNone(self.controller.logger)
        
    def test_executar_conciliacao_sem_dados(self):
        """Testa execução de conciliação sem dados"""
        resultados = self.controller.executar_conciliacao('202512')
        
        self.assertIsInstance(resultados, list)
        # Deve retornar resultados mesmo sem dados (com totais zero)
        self.assertTrue(len(resultados) > 0)
        
    def test_executar_conciliacao_com_dados(self):
        """Testa execução de conciliação com dados simulados"""
        # Cria estrutura de dados de teste
        pasta_mes = os.path.join(self.temp_dir, '072025')
        os.makedirs(pasta_mes)
        
        # Cria arquivos de teste com dados válidos
        test_files = {
            'faturamento_C6_072025.csv': pd.DataFrame({
                'Data da Venda': ['01/07/2025', '02/07/2025'],
                'Valor da Venda': ['R$ 100,50', 'R$ 200,75'],
                'Cliente': ['Cliente A', 'Cliente B']
            }),
            'faturamento_GDS_072025.csv': pd.DataFrame({
                'Data Venda': ['01/07/2025', '02/07/2025'],
                'Valor Venda': ['150,25', '250,30'],
                'Cliente': ['Cliente C', 'Cliente D']
            }),
            'pagamento_C6_072025.csv': pd.DataFrame({
                'Data do Recebível': ['01/07/2025', '02/07/2025'],
                'Valor Recebível': ['R$ 95,00', 'R$ 190,50'],
                'Descontos': ['R$ 5,50', 'R$ 10,25']
            }),
            'pagamento_GDS_072025.csv': pd.DataFrame({
                'Data Pagamento': ['01/07/2025', '02/07/2025'],
                'Valor Pagamento': ['140,75', '235,80'],
                'Cliente': ['Cliente C', 'Cliente D']
            })
        }
        
        for filename, content in test_files.items():
            filepath = os.path.join(pasta_mes, filename)
            content.to_csv(filepath, index=False)
            
        # Executa conciliação
        resultados = self.controller.executar_conciliacao('072025')
        
        self.assertIsInstance(resultados, list)
        self.assertTrue(len(resultados) > 0)
        
        # Verifica se pelo menos um resultado tem dados processados
        has_data = any(r.registros_fonte_1 > 0 or r.registros_fonte_2 > 0 for r in resultados)
        self.assertTrue(has_data)
        
    def test_obter_resumo_dados_sem_dados(self):
        """Testa obtenção de resumo sem dados"""
        resumo = self.controller.obter_resumo_dados('202512')
        
        self.assertIsInstance(resumo, dict)
        # Deve conter chaves para todas as fontes esperadas
        expected_keys = ['faturamento_c6', 'faturamento_gds', 'faturamento_wab', 
                        'pagamento_c6', 'pagamento_gds']
        
        for key in expected_keys:
            self.assertIn(key, resumo)
            
    def test_obter_detalhes_fonte_inexistente(self):
        """Testa obtenção de detalhes para fonte inexistente"""
        detalhes = self.controller.obter_detalhes_fonte('072025', 'fonte_inexistente')
        
        self.assertIn('erro', detalhes)
        self.assertIn('não encontrada', detalhes['erro'])
        
    def test_obter_detalhes_fonte_vazia(self):
        """Testa obtenção de detalhes para fonte vazia"""
        # Cria pasta sem arquivos
        pasta_mes = os.path.join(self.temp_dir, '072025')
        os.makedirs(pasta_mes)
        
        detalhes = self.controller.obter_detalhes_fonte('072025', 'faturamento_c6')
        
        self.assertIn('erro', detalhes)
        
    def test_obter_detalhes_fonte_com_dados(self):
        """Testa obtenção de detalhes para fonte com dados"""
        # Cria dados de teste
        pasta_mes = os.path.join(self.temp_dir, '072025')
        os.makedirs(pasta_mes)
        
        test_data = pd.DataFrame({
            'Data da Venda': ['01/07/2025', '02/07/2025', '03/07/2025'],
            'Valor da Venda': ['R$ 100,50', 'R$ 200,75', 'R$ 150,25'],
            'Cliente': ['Cliente A', 'Cliente B', 'Cliente C']
        })
        
        filepath = os.path.join(pasta_mes, 'faturamento_C6_072025.csv')
        test_data.to_csv(filepath, index=False)
        
        detalhes = self.controller.obter_detalhes_fonte('072025', 'faturamento_c6')
        
        # Verifica estrutura do resultado
        self.assertNotIn('erro', detalhes)
        self.assertIn('registros', detalhes)
        self.assertIn('colunas', detalhes)
        self.assertIn('estatisticas', detalhes)
        self.assertIn('total_principal', detalhes)
        self.assertIn('tipo_total', detalhes)
        
        # Verifica valores
        self.assertEqual(detalhes['registros'], 3)
        self.assertEqual(detalhes['tipo_total'], 'Valor Faturado')
        self.assertGreater(detalhes['total_principal'], 0)
        
    def test_obter_detalhes_fonte_pagamento(self):
        """Testa obtenção de detalhes para fonte de pagamento"""
        # Cria dados de teste para pagamento
        pasta_mes = os.path.join(self.temp_dir, '072025')
        os.makedirs(pasta_mes)
        
        test_data = pd.DataFrame({
            'Data do Recebível': ['01/07/2025', '02/07/2025'],
            'Valor Recebível': ['R$ 95,00', 'R$ 190,50'],
            'Descontos': ['R$ 5,00', 'R$ 9,50']
        })
        
        filepath = os.path.join(pasta_mes, 'pagamento_C6_072025.csv')
        test_data.to_csv(filepath, index=False)
        
        detalhes = self.controller.obter_detalhes_fonte('072025', 'pagamento_c6')
        
        # Verifica se identificou corretamente como pagamento
        self.assertEqual(detalhes['tipo_total'], 'Valor Recebível')
        self.assertGreater(detalhes['total_principal'], 0)
        
    def test_verificar_dados_carregados(self):
        """Testa verificação de dados carregados"""
        # Teste com dados vazios
        dados_vazios = {
            'faturamento_c6': pd.DataFrame(),
            'faturamento_gds': pd.DataFrame()
        }
        
        # Este método é privado, então vamos testar indiretamente através de executar_conciliacao
        # Se não levantar exceção, está funcionando
        try:
            self.controller._verificar_dados_carregados(dados_vazios)
            # Não deve levantar exceção para dados vazios, apenas loggar warnings
        except Exception as e:
            self.fail(f"_verificar_dados_carregados levantou exceção inesperada: {e}")
            
        # Teste com dados válidos
        dados_validos = {
            'faturamento_c6': pd.DataFrame({'col1': [1, 2]}),
            'faturamento_gds': pd.DataFrame({'col1': [3, 4]})
        }
        
        try:
            self.controller._verificar_dados_carregados(dados_validos)
        except Exception as e:
            self.fail(f"_verificar_dados_carregados levantou exceção inesperada: {e}")

if __name__ == '__main__':
    unittest.main()
