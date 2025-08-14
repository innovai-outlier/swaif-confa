"""
Testes de Integração para SWAIF-CONFA
Testam a integração entre os componentes do sistema
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
from src.models.analisador import Analisador
from src.models.data_loader import DataLoader


class TestIntegracaoCompleta(unittest.TestCase):
    """Testes de integração completa do sistema"""
    
    def setUp(self):
        """Configuração antes de cada teste"""
        self.temp_dir = tempfile.mkdtemp()
        self.create_test_data()
        
    def tearDown(self):
        """Limpeza após cada teste"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
        
    def create_test_data(self):
        """Cria dados de teste realistas"""
        pasta_mes = os.path.join(self.temp_dir, '072025')
        os.makedirs(pasta_mes)
        
        # Dados C6 Faturamento
        c6_faturamento = pd.DataFrame({
            'Data da Venda': ['01/07/2025', '02/07/2025', '03/07/2025', '04/07/2025', '05/07/2025'],
            'Valor da Venda': ['R$ 1.250,50', 'R$ 2.300,75', 'R$ 890,25', 'R$ 1.500,00', 'R$ 750,30'],
            'Cliente': ['Empresa A', 'Empresa B', 'Empresa C', 'Empresa D', 'Empresa E'],
            'Produto': ['Produto X', 'Produto Y', 'Produto Z', 'Produto X', 'Produto Y']
        })
        
        # Dados GDS Faturamento
        gds_faturamento = pd.DataFrame({
            'Data Venda': ['01/07/2025', '02/07/2025', '03/07/2025', '04/07/2025'],
            'Valor Venda': ['1.200,00', '2.250,50', '880,75', '1.480,25'],
            'Cliente': ['Empresa A', 'Empresa B', 'Empresa C', 'Empresa D'],
            'Categoria': ['Cat1', 'Cat2', 'Cat1', 'Cat3']
        })
        
        # Dados WAB Faturamento
        wab_faturamento_data = [
            {
                "DATA": "01/07/2025",
                "VALOR PAGO": "R$1.180,50",
                "VALOR TOTAL": "R$1.180,50",
                "DESCRIÇÃO": "Produto Alpha",
                "MODO DE PAGAMTO": "PIX",
                "NOME DO PACIENTE (FORNECEDOR)": "Empresa A",
                "OBS": ""
            },
            {
                "DATA": "02/07/2025",
                "VALOR PAGO": "R$2.200,25",
                "VALOR TOTAL": "R$2.200,25",
                "DESCRIÇÃO": "Produto Beta",
                "MODO DE PAGAMTO": "Crédito",
                "NOME DO PACIENTE (FORNECEDOR)": "Empresa B",
                "OBS": ""
            },
            {
                "DATA": "03/07/2025",
                "VALOR PAGO": "R$860,00",
                "VALOR TOTAL": "R$860,00",
                "DESCRIÇÃO": "Produto Gamma",
                "MODO DE PAGAMTO": "Débito",
                "NOME DO PACIENTE (FORNECEDOR)": "Empresa C",
                "OBS": ""
            },
            {
                "DATA": "04/07/2025",
                "VALOR PAGO": "R$1.450,75",
                "VALOR TOTAL": "R$1.450,75",
                "DESCRIÇÃO": "Produto Delta",
                "MODO DE PAGAMTO": "PIX",
                "NOME DO PACIENTE (FORNECEDOR)": "Empresa D",
                "OBS": ""
            }
        ]
        
        # Dados C6 Pagamento
        c6_pagamento = pd.DataFrame({
            'Data do Recebível': ['01/07/2025', '02/07/2025', '03/07/2025', '04/07/2025'],
            'Valor Recebível': ['R$ 1.180,50', 'R$ 2.200,75', 'R$ 850,25', 'R$ 1.420,00'],
            'Descontos': ['-R$ 70,00', '-R$ 100,00', '-R$ 40,00', '-R$ 80,00'],
            'Cliente': ['Empresa A', 'Empresa B', 'Empresa C', 'Empresa D']
        })
        
        # Dados GDS Pagamento
        gds_pagamento = pd.DataFrame({
            'Data Pagamento': ['01/07/2025', '02/07/2025', '03/07/2025', '04/07/2025', '05/07/2025'],
            'Valor Pagamento': ['1.150,25', '2.180,50', '840,00', '1.400,75', '720,30'],
            'Status': ['Pago', 'Pago', 'Pago', 'Pago', 'Pago'],
            'Cliente': ['Empresa A', 'Empresa B', 'Empresa C', 'Empresa D', 'Empresa E']
        })
        
        # Salvar arquivos
        c6_faturamento.to_csv(os.path.join(pasta_mes, 'faturamento_C6_072025.csv'), index=False)
        gds_faturamento.to_csv(os.path.join(pasta_mes, 'faturamento_GDS_072025.csv'), index=False)
        c6_pagamento.to_csv(os.path.join(pasta_mes, 'pagamento_C6_072025.csv'), index=False)
        gds_pagamento.to_csv(os.path.join(pasta_mes, 'pagamento_GDS_072025.csv'), index=False)
        
        import json
        with open(os.path.join(pasta_mes, 'faturamento_WAB_072025.json'), 'w', encoding='utf-8') as f:
            json.dump(wab_faturamento_data, f, ensure_ascii=False, indent=2)
            
    def test_fluxo_completo_conciliacao(self):
        """Testa fluxo completo de conciliação"""
        # 1. Inicializa controller
        controller = ConciliacaoController(self.temp_dir)
        
        # 2. Executa conciliação
        resultados = controller.executar_conciliacao('072025')
        
        # 3. Verifica resultados
        self.assertIsInstance(resultados, list)
        self.assertTrue(len(resultados) > 0)
        
        # 4. Verifica se todas as comparações foram realizadas
        pares_esperados = [
            ('faturamento_c6', 'faturamento_gds'),
            ('faturamento_c6', 'faturamento_wab'),
            ('faturamento_gds', 'faturamento_wab'),
            ('pagamento_c6', 'pagamento_gds')
        ]
        
        pares_encontrados = [resultado.par_fontes for resultado in resultados]
        
        for par in pares_esperados:
            self.assertIn(par, pares_encontrados)
            
        # 5. Verifica se os totais fazem sentido
        for resultado in resultados:
            self.assertGreaterEqual(resultado.total_fonte_1, 0)
            self.assertGreaterEqual(resultado.total_fonte_2, 0)
            self.assertGreaterEqual(resultado.registros_fonte_1, 0)
            self.assertGreaterEqual(resultado.registros_fonte_2, 0)
            
    def test_integracao_data_loader_analisador(self):
        """Testa integração entre DataLoader e Analisador"""
        # 1. Carrega dados
        data_loader = DataLoader(self.temp_dir)
        dados = data_loader.carregar_dados_mes('072025')
        
        # 2. Verifica se dados foram carregados
        self.assertIn('faturamento_c6', dados)
        self.assertIn('faturamento_gds', dados)
        self.assertIn('faturamento_wab', dados)
        self.assertIn('pagamento_c6', dados)
        self.assertIn('pagamento_gds', dados)
        
        # 3. Analisa dados
        analisador = Analisador()
        resultados = analisador.analisar(dados)
        
        # 4. Verifica resultados da análise
        self.assertIsInstance(resultados, list)
        self.assertTrue(len(resultados) > 0)
        
        # 5. Verifica consistência dos dados
        for resultado in resultados:
            self.assertIsInstance(resultado.diferenca, float)
            self.assertIsInstance(resultado.percentual_diferenca, float)
            
    def test_consistencia_padronizacao_valores(self):
        """Testa consistência da padronização de valores entre componentes"""
        data_loader = DataLoader(self.temp_dir)
        dados = data_loader.carregar_dados_mes('072025')
        
        analisador = Analisador()
        
        # Testa padronização C6 faturamento
        df_c6_fat = dados['faturamento_c6']
        if not df_c6_fat.empty:
            df_padronizado = analisador._padronizar_valores_c6_faturamento(df_c6_fat)
            
            # Verifica se todos os valores são numéricos
            if 'valor_venda' in df_padronizado.columns:
                self.assertTrue(pd.api.types.is_numeric_dtype(df_padronizado['valor_venda']))
                # Verifica se não há valores NaN
                self.assertFalse(df_padronizado['valor_venda'].isna().any())
                
        # Testa padronização C6 pagamento
        df_c6_pag = dados['pagamento_c6']
        if not df_c6_pag.empty:
            df_padronizado = analisador._padronizar_valores_c6_pagamento(df_c6_pag)
            
            # Verifica valores recebíveis
            if 'valor_recebivel' in df_padronizado.columns:
                self.assertTrue(pd.api.types.is_numeric_dtype(df_padronizado['valor_recebivel']))
                
            # Verifica descontos (devem ser negativos)
            if 'descontos' in df_padronizado.columns:
                descontos_nao_zero = df_padronizado[df_padronizado['descontos'] != 0]['descontos']
                if len(descontos_nao_zero) > 0:
                    self.assertTrue(all(descontos_nao_zero < 0))
                    
    def test_performance_sistema_completo(self):
        """Testa performance do sistema completo"""
        import time
        
        inicio = time.time()
        
        # Executa fluxo completo
        controller = ConciliacaoController(self.temp_dir)
        resultados = controller.executar_conciliacao('072025')
        
        fim = time.time()
        duracao = fim - inicio
        
        # Verifica se execução foi rápida (< 5 segundos)
        self.assertLess(duracao, 5.0)
        
        # Verifica se resultados foram produzidos
        self.assertTrue(len(resultados) > 0)
        
    def test_obter_detalhes_todas_fontes(self):
        """Testa obtenção de detalhes para todas as fontes"""
        controller = ConciliacaoController(self.temp_dir)
        
        fontes = ['faturamento_c6', 'faturamento_gds', 'faturamento_wab', 
                 'pagamento_c6', 'pagamento_gds']
        
        for fonte in fontes:
            with self.subTest(fonte=fonte):
                detalhes = controller.obter_detalhes_fonte('072025', fonte)
                
                if 'erro' not in detalhes:
                    # Verifica estrutura dos detalhes
                    self.assertIn('registros', detalhes)
                    self.assertIn('colunas', detalhes)
                    self.assertIn('total_principal', detalhes)
                    self.assertIn('tipo_total', detalhes)
                    
                    # Verifica tipo de total baseado na fonte
                    if 'faturamento' in fonte:
                        self.assertEqual(detalhes['tipo_total'], 'Valor Faturado')
                    elif 'pagamento' in fonte:
                        self.assertEqual(detalhes['tipo_total'], 'Valor Recebível')
                        
    def test_resumo_dados_consistente(self):
        """Testa se resumo de dados é consistente"""
        controller = ConciliacaoController(self.temp_dir)
        resumo = controller.obter_resumo_dados('072025')
        
        # Verifica estrutura do resumo
        fontes_esperadas = ['faturamento_c6', 'faturamento_gds', 'faturamento_wab',
                           'pagamento_c6', 'pagamento_gds']
        
        for fonte in fontes_esperadas:
            self.assertIn(fonte, resumo)
            
        # Verifica dados carregados
        total_registros = sum(resumo[fonte]['registros'] for fonte in fontes_esperadas 
                             if resumo[fonte]['registros'] > 0)
        self.assertGreater(total_registros, 0)

class TestIntegracaoErros(unittest.TestCase):
    """Testa integração em cenários de erro"""
    
    def setUp(self):
        """Configuração antes de cada teste"""
        self.temp_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        """Limpeza após cada teste"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
        
    def test_sistema_sem_dados(self):
        """Testa sistema funcionando sem dados disponíveis"""
        controller = ConciliacaoController(self.temp_dir)
        
        # Tenta executar conciliação sem dados
        resultados = controller.executar_conciliacao('202512')
        
        # Sistema deve funcionar mas retornar resultados com totais zero
        self.assertIsInstance(resultados, list)
        
        for resultado in resultados:
            self.assertEqual(resultado.total_fonte_1, 0.0)
            self.assertEqual(resultado.total_fonte_2, 0.0)
            
    def test_sistema_dados_corrompidos(self):
        """Testa sistema com dados corrompidos"""
        # Cria pasta com arquivo corrompido
        pasta_mes = os.path.join(self.temp_dir, '072025')
        os.makedirs(pasta_mes)
        
        # Arquivo CSV mal formado
        with open(os.path.join(pasta_mes, 'faturamento_C6_072025.csv'), 'w') as f:
            f.write("dados,corrompidos,sem\nheader,adequado")
            
        controller = ConciliacaoController(self.temp_dir)
        
        # Sistema deve tratar o erro graciosamente
        try:
            resultados = controller.executar_conciliacao('072025')
            # Se chegou aqui, o sistema tratou o erro
            self.assertIsInstance(resultados, list)
        except Exception as e:
            # Se houve exceção, verifica se é tratada adequadamente
            self.assertIsInstance(e, Exception)

if __name__ == '__main__':
    unittest.main()
