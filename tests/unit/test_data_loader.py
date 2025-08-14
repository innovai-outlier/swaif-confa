"""
Testes Unitários para o Data Loader
"""
import unittest
import pandas as pd
import tempfile
import os
from unittest.mock import patch, MagicMock
import sys

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.models.data_loader import DataLoader

class TestDataLoader(unittest.TestCase):
    """Testes para o componente DataLoader"""
    
    def setUp(self):
        """Configuração antes de cada teste"""
        self.temp_dir = tempfile.mkdtemp()
        self.data_loader = DataLoader(self.temp_dir)
        
    def tearDown(self):
        """Limpeza após cada teste"""
        # Remove arquivos temporários
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
        
    def test_init_data_loader(self):
        """Testa inicialização do DataLoader"""
        self.assertEqual(self.data_loader.base_path, self.temp_dir)
        self.assertIsNotNone(self.data_loader.logger)
        
    def test_get_pasta_mes(self):
        """Testa método de obtenção da pasta do mês"""
        # Testa diferentes formatos de entrada
        test_cases = [
            ('072025', '072025'),
            ('07', '07'),
            ('julho', 'julho')
        ]
        
        for input_mes, expected in test_cases:
            with self.subTest(input_mes=input_mes):
                result = self.data_loader._get_pasta_mes(input_mes)
                self.assertEqual(result, expected)
                
    def test_ler_csv_arquivo_inexistente(self):
        """Testa leitura de arquivo CSV inexistente"""
        arquivo_inexistente = os.path.join(self.temp_dir, "inexistente.csv")
        resultado = self.data_loader.ler_csv(arquivo_inexistente)
        
        self.assertTrue(resultado.empty)
        
    def test_ler_csv_arquivo_valido(self):
        """Testa leitura de arquivo CSV válido"""
        # Cria arquivo CSV de teste
        test_csv = os.path.join(self.temp_dir, "teste.csv")
        test_data = pd.DataFrame({
            'coluna1': [1, 2, 3],
            'coluna2': ['A', 'B', 'C'],
            'valor': [10.5, 20.3, 30.1]
        })
        test_data.to_csv(test_csv, index=False)
        
        resultado = self.data_loader.ler_csv(test_csv)
        
        self.assertFalse(resultado.empty)
        self.assertEqual(len(resultado), 3)
        self.assertIn('coluna1', resultado.columns)
        
    def test_ler_wab_json_arquivo_inexistente(self):
        """Testa leitura de arquivo WAB JSON inexistente"""
        resultado = self.data_loader.ler_wab_json('arquivo_inexistente.json')
        self.assertTrue(resultado.empty)

    def test_ler_wab_json_arquivo_valido(self):
        """Testa leitura de arquivo WAB JSON válido"""
        # Cria arquivo JSON temporário
        test_data = [
            {
                "DATA": "01/07/2025",
                "VALOR PAGO": "R$100,00",
                "VALOR TOTAL": "R$100,00",
                "DESCRIÇÃO": "Teste",
                "MODO DE PAGAMTO": "PIX",
                "NOME DO PACIENTE (FORNECEDOR)": "Cliente Teste",
                "OBS": ""
            }
        ]
        
        import json
        test_file = os.path.join(self.temp_dir, 'test_wab.json')
        with open(test_file, 'w', encoding='utf-8') as f:
            json.dump(test_data, f, ensure_ascii=False, indent=2)
        
        resultado = self.data_loader.ler_wab_json(test_file)
        
        self.assertFalse(resultado.empty)
        self.assertEqual(len(resultado), 1)
        self.assertIn('data', resultado.columns)
        self.assertIn('valor_pago', resultado.columns)

    def test_converter_wab_txt_para_json(self):
        """Testa conversão de WAB TXT para JSON (funcionalidade de migração)"""
        # Cria arquivo TXT de teste no formato WAB real
        test_txt = os.path.join(self.temp_dir, "teste_wab.txt")
        with open(test_txt, 'w', encoding='utf-8') as f:
            f.write("DATA: 01/07/2025\n")
            f.write("VALOR PAGO: R$100,00\n")
            f.write("VALOR TOTAL: R$100,00\n")
            f.write("DESCRIÇÃO: Teste\n")
            f.write("MODO DE PAGAMTO: PIX\n")
            f.write("NOME DO PACIENTE (FORNECEDOR): Cliente Teste\n")
            f.write("OBS: \n")
            f.write("\n")
            f.write("DATA: 02/07/2025\n")
            f.write("VALOR PAGO: R$200,50\n")
            f.write("VALOR TOTAL: R$200,50\n")
            f.write("DESCRIÇÃO: Teste 2\n")
            f.write("MODO DE PAGAMTO: Débito\n")
            f.write("NOME DO PACIENTE (FORNECEDOR): Cliente Teste 2\n")
            f.write("OBS: Observação\n")
        
        # Converte para JSON
        json_path = self.data_loader.converter_wab_txt_para_json(test_txt)
        
        # Verifica se a conversão foi bem-sucedida
        self.assertIsNotNone(json_path)
        self.assertTrue(os.path.exists(json_path))
        
        # Verifica o conteúdo do JSON
        import json
        with open(json_path, 'r', encoding='utf-8') as f:
            dados = json.load(f)
        
        self.assertEqual(len(dados), 2)
        self.assertEqual(dados[0]['DATA'], '01/07/2025')
        self.assertEqual(dados[0]['VALOR PAGO'], 'R$100,00')
        self.assertEqual(dados[1]['VALOR PAGO'], 'R$200,50')

    def test_mapear_colunas_c6_faturamento(self):
        """Testa mapeamento de colunas C6 faturamento"""
        # Cria DataFrame com colunas originais
        df_original = pd.DataFrame({
            'Data da Venda': ['01/07/2025', '02/07/2025'],
            'Valor da Venda': [100.0, 200.0],
            'Cliente': ['Cliente A', 'Cliente B']
        })
        
        resultado = self.data_loader._mapear_colunas(df_original, 'faturamento_C6')
        
        self.assertIn('data_venda', resultado.columns)
        self.assertIn('valor_venda', resultado.columns)
        self.assertIn('cliente', resultado.columns)
        
    def test_mapear_colunas_fonte_inexistente(self):
        """Testa mapeamento com fonte inexistente"""
        df_test = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
        
        resultado = self.data_loader._mapear_colunas(df_test, 'fonte_inexistente')
        
        # Deve retornar o DataFrame original se não houver mapeamento
        pd.testing.assert_frame_equal(resultado, df_test)
        
    def test_carregar_dados_mes_pasta_inexistente(self):
        """Testa carregamento de dados para pasta inexistente"""
        resultado = self.data_loader.carregar_dados_mes('202512')  # mês futuro
        
        # Deve retornar dicionário com DataFrames vazios
        self.assertIsInstance(resultado, dict)
        for fonte, df in resultado.items():
            self.assertTrue(df.empty)
            
    def test_carregar_dados_mes_com_arquivos(self):
        """Testa carregamento de dados com arquivos presentes"""
        # Cria estrutura de diretório de teste
        pasta_mes = os.path.join(self.temp_dir, '072025')
        os.makedirs(pasta_mes)
        
        # Cria arquivos de teste
        test_files = {
            'faturamento_C6_072025.csv': pd.DataFrame({
                'Data da Venda': ['01/07/2025'],
                'Valor da Venda': [100.0]
            }),
            'faturamento_GDS_072025.csv': pd.DataFrame({
                'Data Venda': ['01/07/2025'],
                'Valor Venda': [200.0]
            }),
            'faturamento_WAB_072025.json': [
                {
                    "DATA": "01/07/2025",
                    "VALOR PAGO": "R$15,50",
                    "VALOR TOTAL": "R$15,50",
                    "DESCRIÇÃO": "Produto A",
                    "MODO DE PAGAMTO": "PIX",
                    "NOME DO PACIENTE (FORNECEDOR)": "Cliente Teste",
                    "OBS": ""
                }
            ]
        }
        
        for filename, content in test_files.items():
            filepath = os.path.join(pasta_mes, filename)
            if filename.endswith('.csv'):
                content.to_csv(filepath, index=False)
            elif filename.endswith('.json'):
                import json
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(content, f, ensure_ascii=False, indent=2)
            else:
                with open(filepath, 'w') as f:
                    f.write(content)
                    
        resultado = self.data_loader.carregar_dados_mes('072025')
        
        # Verifica se os dados foram carregados
        self.assertIn('faturamento_c6', resultado)
        self.assertIn('faturamento_gds', resultado)
        self.assertIn('faturamento_wab', resultado)
        
        # Verifica se os DataFrames não estão vazios
        self.assertFalse(resultado['faturamento_c6'].empty)
        self.assertFalse(resultado['faturamento_gds'].empty)
        self.assertFalse(resultado['faturamento_wab'].empty)

if __name__ == '__main__':
    unittest.main()
