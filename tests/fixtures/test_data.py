"""
Fixtures para Testes - Dados de Teste Padronizados
"""
import os
import tempfile
from typing import Dict

import pandas as pd


class TestDataFixtures:
    """Classe para gerar dados de teste consistentes"""
    
    @staticmethod
    def create_c6_faturamento_data() -> pd.DataFrame:
        """Cria dados de teste para C6 faturamento"""
        return pd.DataFrame({
            'Data da Venda': ['01/07/2025', '02/07/2025', '03/07/2025', '04/07/2025', '05/07/2025'],
            'Valor da Venda': ['R$ 1.250,50', 'R$ 2.300,75', 'R$ 890,25', 'R$ 1.500,00', 'R$ 750,30'],
            'Cliente': ['Empresa A', 'Empresa B', 'Empresa C', 'Empresa D', 'Empresa E'],
            'Produto': ['Produto X', 'Produto Y', 'Produto Z', 'Produto X', 'Produto Y'],
            'Status': ['Faturado', 'Faturado', 'Faturado', 'Faturado', 'Faturado']
        })
    
    @staticmethod
    def create_gds_faturamento_data() -> pd.DataFrame:
        """Cria dados de teste para GDS faturamento"""
        return pd.DataFrame({
            'Data Venda': ['01/07/2025', '02/07/2025', '03/07/2025', '04/07/2025', '05/07/2025'],
            'Valor Venda': ['1.200,00', '2.250,50', '880,75', '1.480,25', '720,30'],
            'Cliente': ['Empresa A', 'Empresa B', 'Empresa C', 'Empresa D', 'Empresa E'],
            'Categoria': ['Cat1', 'Cat2', 'Cat1', 'Cat3', 'Cat2'],
            'Status': ['Ativo', 'Ativo', 'Ativo', 'Ativo', 'Ativo']
        })
    
    @staticmethod
    def create_wab_faturamento_data() -> dict:
        """Cria dados de teste para WAB faturamento (formato JSON)"""
        return [
            {
                "DATA": "01/07/2025",
                "VALOR PAGO": "R$1.180,50",
                "VALOR TOTAL": "R$1.180,50",
                "DESCRIÇÃO": "Pagamento de consulta",
                "MODO DE PAGAMTO": "PIX",
                "NOME DO PACIENTE (FORNECEDOR)": "Empresa A Ltda",
                "OBS": ""
            },
            {
                "DATA": "02/07/2025",
                "VALOR PAGO": "R$2.200,25",
                "VALOR TOTAL": "R$2.200,25",
                "DESCRIÇÃO": "Pagamento de procedimento",
                "MODO DE PAGAMTO": "Crédito (VISA)",
                "NOME DO PACIENTE (FORNECEDOR)": "Empresa B Corp",
                "OBS": "Parcelado em 3x"
            },
            {
                "DATA": "03/07/2025",
                "VALOR PAGO": "R$860,00",
                "VALOR TOTAL": "R$860,00",
                "DESCRIÇÃO": "Pagamento de exame",
                "MODO DE PAGAMTO": "Débito",
                "NOME DO PACIENTE (FORNECEDOR)": "Cliente C Silva",
                "OBS": ""
            },
            {
                "DATA": "04/07/2025",
                "VALOR PAGO": "R$1.450,75",
                "VALOR TOTAL": "R$1.450,75",
                "DESCRIÇÃO": "Pagamento de tratamento",
                "MODO DE PAGAMTO": "PIX",
                "NOME DO PACIENTE (FORNECEDOR)": "Paciente D Santos",
                "OBS": ""
            },
            {
                "DATA": "05/07/2025",
                "VALOR PAGO": "R$710,25",
                "VALOR TOTAL": "R$710,25",
                "DESCRIÇÃO": "Pagamento de consulta",
                "MODO DE PAGAMTO": "Dinheiro",
                "NOME DO PACIENTE (FORNECEDOR)": "Cliente E Lima",
                "OBS": "Pagamento à vista"
            }
        ]
    
    @staticmethod
    def create_c6_pagamento_data() -> pd.DataFrame:
        """Cria dados de teste para C6 pagamento"""
        return pd.DataFrame({
            'Data do Recebível': ['01/07/2025', '02/07/2025', '03/07/2025', '04/07/2025', '05/07/2025'],
            'Valor Recebível': ['R$ 1.180,50', 'R$ 2.200,75', 'R$ 850,25', 'R$ 1.420,00', 'R$ 720,30'],
            'Descontos': ['-R$ 70,00', '-R$ 100,00', '-R$ 40,00', '-R$ 80,00', '-R$ 30,00'],
            'Cliente': ['Empresa A', 'Empresa B', 'Empresa C', 'Empresa D', 'Empresa E'],
            'Status Pagamento': ['Recebido', 'Recebido', 'Recebido', 'Recebido', 'Recebido']
        })
    
    @staticmethod
    def create_gds_pagamento_data() -> pd.DataFrame:
        """Cria dados de teste para GDS pagamento"""
        return pd.DataFrame({
            'Data Pagamento': ['01/07/2025', '02/07/2025', '03/07/2025', '04/07/2025', '05/07/2025'],
            'Valor Pagamento': ['1.150,25', '2.180,50', '840,00', '1.400,75', '700,30'],
            'Status': ['Pago', 'Pago', 'Pago', 'Pago', 'Pago'],
            'Cliente': ['Empresa A', 'Empresa B', 'Empresa C', 'Empresa D', 'Empresa E'],
            'Metodo': ['PIX', 'TED', 'PIX', 'TED', 'PIX']
        })
    
    @staticmethod
    def create_test_environment(base_path: str, mes_ano: str = '072025') -> str:
        """
        Cria ambiente de teste completo
        
        Args:
            base_path: Caminho base para criar os dados
            mes_ano: Mês/ano no formato MMAAAA
            
        Returns:
            Caminho da pasta criada
        """
        pasta_mes = os.path.join(base_path, mes_ano)
        os.makedirs(pasta_mes, exist_ok=True)
        
        # Criar arquivos de teste
        fixtures = TestDataFixtures()
        
        # C6 Faturamento
        c6_fat = fixtures.create_c6_faturamento_data()
        c6_fat.to_csv(os.path.join(pasta_mes, f'faturamento_C6_{mes_ano}.csv'), index=False)
        
        # GDS Faturamento
        gds_fat = fixtures.create_gds_faturamento_data()
        gds_fat.to_csv(os.path.join(pasta_mes, f'faturamento_GDS_{mes_ano}.csv'), index=False)
        
        # WAB Faturamento
        wab_data = fixtures.create_wab_faturamento_data()
        import json
        with open(os.path.join(pasta_mes, f'faturamento_WAB_{mes_ano}.json'), 'w', encoding='utf-8') as f:
            json.dump(wab_data, f, ensure_ascii=False, indent=2)
        
        # C6 Pagamento
        c6_pag = fixtures.create_c6_pagamento_data()
        c6_pag.to_csv(os.path.join(pasta_mes, f'pagamento_C6_{mes_ano}.csv'), index=False)
        
        # GDS Pagamento
        gds_pag = fixtures.create_gds_pagamento_data()
        gds_pag.to_csv(os.path.join(pasta_mes, f'pagamento_GDS_{mes_ano}.csv'), index=False)
        
        return pasta_mes
    
    @staticmethod
    def get_expected_totals() -> Dict[str, float]:
        """Retorna totais esperados para validação"""
        return {
            'faturamento_c6': 6691.80,    # Soma dos valores de venda
            'faturamento_gds': 6531.80,   # Soma dos valores GDS
            'faturamento_wab': 6401.75,   # Soma dos valores WAB
            'pagamento_c6': 6371.80,      # Soma dos valores recebíveis
            'pagamento_gds': 6271.80      # Soma dos valores pagamento
        }
    
    @staticmethod
    def get_expected_records() -> Dict[str, int]:
        """Retorna número de registros esperados para validação"""
        return {
            'faturamento_c6': 5,
            'faturamento_gds': 5,
            'faturamento_wab': 5,
            'pagamento_c6': 5,
            'pagamento_gds': 5
        }
    
    @staticmethod
    def create_corrupted_data_environment(base_path: str, mes_ano: str = '072025') -> str:
        """
        Cria ambiente com dados corrompidos para teste de robustez
        
        Args:
            base_path: Caminho base
            mes_ano: Mês/ano no formato MMAAAA
            
        Returns:
            Caminho da pasta criada
        """
        pasta_mes = os.path.join(base_path, mes_ano)
        os.makedirs(pasta_mes, exist_ok=True)
        
        # Arquivo CSV mal formado
        corrupted_csv = os.path.join(pasta_mes, f'faturamento_C6_{mes_ano}.csv')
        with open(corrupted_csv, 'w') as f:
            f.write("dados,sem,header\nvalor,incorreto,formato\n")
        
        # Arquivo com dados inválidos
        invalid_data = pd.DataFrame({
            'Data da Venda': ['data_invalida', '32/13/2025'],
            'Valor da Venda': ['valor_texto', 'R$ abc,def'],
            'Cliente': ['', None]
        })
        invalid_data.to_csv(os.path.join(pasta_mes, f'faturamento_GDS_{mes_ano}.csv'), index=False)
        
        # Arquivo WAB vazio
        with open(os.path.join(pasta_mes, f'faturamento_WAB_{mes_ano}.json'), 'w') as f:
            f.write("[]")
        
        return pasta_mes
    
    @staticmethod
    def create_minimal_valid_data(base_path: str, mes_ano: str = '072025') -> str:
        """
        Cria conjunto mínimo de dados válidos
        
        Args:
            base_path: Caminho base
            mes_ano: Mês/ano no formato MMAAAA
            
        Returns:
            Caminho da pasta criada
        """
        pasta_mes = os.path.join(base_path, mes_ano)
        os.makedirs(pasta_mes, exist_ok=True)
        
        # Apenas um arquivo com um registro
        minimal_data = pd.DataFrame({
            'Data da Venda': ['01/07/2025'],
            'Valor da Venda': ['R$ 100,00'],
            'Cliente': ['Cliente Teste']
        })
        
        minimal_data.to_csv(os.path.join(pasta_mes, f'faturamento_C6_{mes_ano}.csv'), index=False)
        
        return pasta_mes

class TestContextManager:
    """Context manager para criação/limpeza automática de ambiente de teste"""
    
    def __init__(self, fixture_type: str = 'complete', mes_ano: str = '072025'):
        self.fixture_type = fixture_type
        self.mes_ano = mes_ano
        self.temp_dir = None
        self.pasta_mes = None
        
    def __enter__(self):
        self.temp_dir = tempfile.mkdtemp()
        
        if self.fixture_type == 'complete':
            self.pasta_mes = TestDataFixtures.create_test_environment(self.temp_dir, self.mes_ano)
        elif self.fixture_type == 'corrupted':
            self.pasta_mes = TestDataFixtures.create_corrupted_data_environment(self.temp_dir, self.mes_ano)
        elif self.fixture_type == 'minimal':
            self.pasta_mes = TestDataFixtures.create_minimal_valid_data(self.temp_dir, self.mes_ano)
        
        return self.temp_dir
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.temp_dir:
            import shutil
            shutil.rmtree(self.temp_dir, ignore_errors=True)
