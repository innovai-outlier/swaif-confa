"""
Testes Unitários para o Analisador
"""
import unittest
import pandas as pd
import sys
import os

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.models.analisador import Analisador, ResultadoAnalise

class TestAnalisador(unittest.TestCase):
    """Testes para o componente Analisador"""
    
    def setUp(self):
        """Configuração antes de cada teste"""
        self.analisador = Analisador()
        
    def test_init_analisador(self):
        """Testa inicialização do Analisador"""
        self.assertIsNotNone(self.analisador.logger)
        
    def test_criar_resultado_analise(self):
        """Testa criação de resultado de análise"""
        resultado = ResultadoAnalise(
            par_fontes=('fonte1', 'fonte2'),
            total_fonte_1=1000.0,
            total_fonte_2=1100.0,
            registros_fonte_1=10,
            registros_fonte_2=12,
            diferenca=100.0,
            percentual_diferenca=10.0
        )
        
        self.assertEqual(resultado.par_fontes, ('fonte1', 'fonte2'))
        self.assertEqual(resultado.total_fonte_1, 1000.0)
        self.assertEqual(resultado.diferenca, 100.0)
        
    def test_padronizar_valores_c6_faturamento(self):
        """Testa padronização de valores C6 faturamento"""
        df_test = pd.DataFrame({
            'valor_venda': ['R$ 100,50', 'R$ 200,75', ''],
            'data_venda': ['01/07/2025', '02/07/2025', '03/07/2025']
        })
        
        resultado = self.analisador._padronizar_valores_c6_faturamento(df_test)
        
        # Verifica se valores foram convertidos corretamente
        self.assertEqual(resultado.loc[0, 'valor_venda'], 100.50)
        self.assertEqual(resultado.loc[1, 'valor_venda'], 200.75)
        self.assertEqual(resultado.loc[2, 'valor_venda'], 0.0)  # vazio vira 0
        
        # Verifica se datas foram convertidas
        self.assertEqual(resultado.dtypes['data_venda'], 'datetime64[ns]')
        
    def test_padronizar_valores_c6_pagamento(self):
        """Testa padronização de valores C6 pagamento com negativos"""
        df_test = pd.DataFrame({
            'valor_recebivel': ['R$ 150,25', 'R$ 300,00'],
            'descontos': ['-R$ 10,50', '-R$ 5,25'],
            'data_recebivel': ['01/07/2025', '02/07/2025']
        })
        
        resultado = self.analisador._padronizar_valores_c6_pagamento(df_test)
        
        # Verifica valores positivos
        self.assertEqual(resultado.loc[0, 'valor_recebivel'], 150.25)
        self.assertEqual(resultado.loc[1, 'valor_recebivel'], 300.00)
        
        # Verifica valores negativos (descontos)
        self.assertEqual(resultado.loc[0, 'descontos'], -10.50)
        self.assertEqual(resultado.loc[1, 'descontos'], -5.25)
        
    def test_padronizar_valores_gds(self):
        """Testa padronização de valores GDS"""
        df_test = pd.DataFrame({
            'valor': ['1.500,75', '2.300,50', ''],
            'data': ['01/07/2025', '02/07/2025', '03/07/2025']
        })
        
        resultado = self.analisador._padronizar_valores_gds(df_test)
        
        # Verifica conversão de valores com ponto de milhar
        self.assertEqual(resultado.loc[0, 'valor'], 1500.75)
        self.assertEqual(resultado.loc[1, 'valor'], 2300.50)
        self.assertEqual(resultado.loc[2, 'valor'], 0.0)
        
    def test_padronizar_valores_wab(self):
        """Testa padronização de valores WAB"""
        df_test = pd.DataFrame({
            'valor': [15.50, 25.30, 0.0],
            'data': ['2025-07-01', '2025-07-02', '2025-07-03']
        })
        
        resultado = self.analisador._padronizar_valores_wab(df_test)
        
        # WAB já vem em formato correto, mas verifica se não há alterações indevidas
        self.assertEqual(resultado.loc[0, 'valor'], 15.50)
        self.assertEqual(resultado.loc[1, 'valor'], 25.30)
        
    def test_calcular_totais_faturamento(self):
        """Testa cálculo de totais para faturamento"""
        dados = {
            'faturamento_c6': pd.DataFrame({
                'valor_venda': [100.0, 200.0, 300.0]
            }),
            'faturamento_gds': pd.DataFrame({
                'valor': [150.0, 250.0]
            }),
            'faturamento_wab': pd.DataFrame({
                'valor': [50.0, 75.0, 100.0]
            })
        }
        
        resultado = self.analisador.calcular_totais_faturamento(dados)
        
        self.assertEqual(resultado['faturamento_c6']['total'], 600.0)
        self.assertEqual(resultado['faturamento_c6']['registros'], 3)
        self.assertEqual(resultado['faturamento_gds']['total'], 400.0)
        self.assertEqual(resultado['faturamento_wab']['total'], 225.0)
        
    def test_calcular_totais_pagamento(self):
        """Testa cálculo de totais para pagamento"""
        dados = {
            'pagamento_c6': pd.DataFrame({
                'valor_recebivel': [100.0, 200.0],
                'descontos': [-10.0, -5.0]
            }),
            'pagamento_gds': pd.DataFrame({
                'valor': [150.0, 250.0, 300.0]
            })
        }
        
        resultado = self.analisador.calcular_totais_pagamento(dados)
        
        # C6 usa valor_recebivel
        self.assertEqual(resultado['pagamento_c6']['total'], 300.0)
        self.assertEqual(resultado['pagamento_c6']['registros'], 2)
        # GDS usa valor
        self.assertEqual(resultado['pagamento_gds']['total'], 700.0)
        self.assertEqual(resultado['pagamento_gds']['registros'], 3)
        
    def test_comparar_fontes(self):
        """Testa comparação entre duas fontes"""
        fonte1_dados = {'total': 1000.0, 'registros': 10}
        fonte2_dados = {'total': 1100.0, 'registros': 11}
        
        resultado = self.analisador._comparar_fontes(
            ('fonte1', 'fonte2'), fonte1_dados, fonte2_dados
        )
        
        self.assertEqual(resultado.par_fontes, ('fonte1', 'fonte2'))
        self.assertEqual(resultado.total_fonte_1, 1000.0)
        self.assertEqual(resultado.total_fonte_2, 1100.0)
        self.assertEqual(resultado.diferenca, 100.0)
        self.assertAlmostEqual(resultado.percentual_diferenca, 10.0, places=1)
        
    def test_comparar_fontes_divisao_por_zero(self):
        """Testa comparação com divisão por zero"""
        fonte1_dados = {'total': 0.0, 'registros': 0}
        fonte2_dados = {'total': 100.0, 'registros': 5}
        
        resultado = self.analisador._comparar_fontes(
            ('fonte1', 'fonte2'), fonte1_dados, fonte2_dados
        )
        
        self.assertEqual(resultado.percentual_diferenca, 0.0)
        
    def test_analisar_dados_vazios(self):
        """Testa análise com dados vazios"""
        dados_vazios = {
            'faturamento_c6': pd.DataFrame(),
            'faturamento_gds': pd.DataFrame(),
            'pagamento_c6': pd.DataFrame(),
            'pagamento_gds': pd.DataFrame()
        }
        
        resultados = self.analisador.analisar(dados_vazios)
        
        # Deve retornar lista de resultados, mas todos com totais zero
        self.assertIsInstance(resultados, list)
        self.assertTrue(len(resultados) > 0)
        
        for resultado in resultados:
            self.assertEqual(resultado.total_fonte_1, 0.0)
            self.assertEqual(resultado.total_fonte_2, 0.0)
            
    def test_analisar_dados_completos(self):
        """Testa análise com dados completos"""
        dados = {
            'faturamento_c6': pd.DataFrame({
                'valor_venda': [100.0, 200.0]
            }),
            'faturamento_gds': pd.DataFrame({
                'valor': [150.0, 250.0]
            }),
            'pagamento_c6': pd.DataFrame({
                'valor_recebivel': [90.0, 180.0]
            }),
            'pagamento_gds': pd.DataFrame({
                'valor': [140.0, 230.0]
            })
        }
        
        resultados = self.analisador.analisar(dados)
        
        self.assertIsInstance(resultados, list)
        self.assertTrue(len(resultados) > 0)
        
        # Verifica se pelo menos um resultado tem valores não-zero
        has_non_zero = any(r.total_fonte_1 > 0 or r.total_fonte_2 > 0 for r in resultados)
        self.assertTrue(has_non_zero)

if __name__ == '__main__':
    unittest.main()
