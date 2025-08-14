"""Data Loader - Modelo para carregamento e padronização dos dados."""
import logging
import os
from typing import Dict, List, Optional

import pandas as pd

from .c6_loader import (
    FATURAMENTO_C6_COLS,
    PAGAMENTO_C6_COLS,
)
from .c6_loader import (
    ler_csv as ler_csv_c6,
)
from .wab_loader import (
    WAB_COLS,
)
from .wab_loader import (
    converter_wab_txt_para_json as wab_converter,
)
from .wab_loader import (
    ler_wab_json as wab_json,
)
from .wab_loader import (
    ler_wab_txt as wab_txt,
)


class DataLoader:
    """Classe responsável pelo carregamento e padronização dos dados de faturamento e pagamento"""
    
    def __init__(self, base_path: str):
        self.base_path = base_path
        self.logger = logging.getLogger(__name__)
        
        # Mapeamentos de colunas para padronização
        self.faturamento_c6_cols = FATURAMENTO_C6_COLS
        
        self.faturamento_gds_cols = {
            'R/D': 'tipo',
            'Data de emissão': 'data_emissao',
            'Data de vencimento': 'data_vencimento',
            'Data de baixa': 'data_baixa',
            'Responsável': 'responsavel',
            'Paciente': 'paciente',
            'Descrição': 'descricao',
            'Serviços': 'servicos',
            'Categoria': 'categoria',
            'Nota fiscal': 'nota_fiscal',
            'Convênio': 'convenio',
            'Método': 'metodo',
            'Caixa': 'caixa',
            'Valor': 'valor',
            'Valor líquido': 'valor_liquido',
            'Agendado': 'agendado',
            'Pago': 'pago',
            'Observações': 'observacoes'
        }
        
        self.pagamento_c6_cols = PAGAMENTO_C6_COLS
        
        self.pagamento_gds_cols = self.faturamento_gds_cols  # Mesma estrutura
        
        self.wab_cols = WAB_COLS

    def ler_csv(
        self, file_path: str, column_mapping: Optional[Dict[str, str]] = None
    ) -> pd.DataFrame:
        """Lê arquivo CSV e aplica mapeamento de colunas."""
        mapping = column_mapping or {}
        return ler_csv_c6(file_path, mapping)

    def ler_wab_txt(self, file_path: str) -> pd.DataFrame:
        """
        Lê o arquivo WAB em formato TXT (LEGADO - usado apenas para conversão inicial)
        
        NOTA: Este método é mantido apenas para conversão de arquivos TXT legacy para JSON.
        Para análises, use sempre o formato JSON através de ler_wab_json().
        
        Args:
            file_path: Caminho para o arquivo TXT do WAB
            
        Returns:
            DataFrame padronizado com dados do WAB
        """
        return wab_txt(file_path)

    def ler_wab_json(self, file_path: str) -> pd.DataFrame:
        """
        Lê o arquivo WAB em formato JSON (formato oficial para análises)
        
        Args:
            file_path: Caminho para o arquivo JSON do WAB
            
        Returns:
            DataFrame padronizado com dados do WAB
        """
        return wab_json(file_path)

    def converter_wab_txt_para_json(self, txt_path: str, json_path: Optional[str] = None) -> Optional[str]:
        """Converte arquivo WAB TXT para JSON."""
        return wab_converter(txt_path, json_path)

    def carregar_dados_mes(self, mes_ano: str) -> Dict[str, pd.DataFrame]:
        """
        Carrega todos os dados de faturamento e pagamento para um mês específico
        
        Args:
            mes_ano: String no formato "072025" (mês + ano)
            
        Returns:
            Dict com DataFrames de cada fonte
        """
        pasta_mes = os.path.join(self.base_path, self._get_pasta_mes(mes_ano))
        
        dados = {}
        
        # Faturamentos
        arquivos_faturamento = {
            'faturamento_c6': (f'faturamento_C6_{mes_ano}.csv', self.faturamento_c6_cols),
            'faturamento_gds': (f'faturamento_GDS_{mes_ano}.csv', self.faturamento_gds_cols),
            'faturamento_wab': (f'faturamento_WAB_{mes_ano}.json', None)  # WAB agora usa JSON exclusivamente
        }
        
        # Pagamentos
        arquivos_pagamento = {
            'pagamento_c6': (f'pagamento_C6_{mes_ano}.csv', self.pagamento_c6_cols),
            'pagamento_gds': (f'pagamento_GDS_{mes_ano}.csv', self.pagamento_gds_cols)
        }
        
        # Carrega faturamentos
        for key, (filename, cols) in arquivos_faturamento.items():
            if key == 'faturamento_wab':
                # Para WAB, usa apenas JSON como fonte oficial
                json_path = os.path.join(pasta_mes, filename)
                
                if os.path.exists(json_path):
                    dados[key] = self.ler_wab_json(json_path)
                else:
                    self.logger.warning(f"Arquivo WAB JSON não encontrado: {json_path}")
                    dados[key] = pd.DataFrame()
            else:
                file_path = os.path.join(pasta_mes, filename)
                if os.path.exists(file_path):
                    dados[key] = self.ler_csv(file_path, cols)
                else:
                    self.logger.warning(f"Arquivo não encontrado: {file_path}")
                    dados[key] = pd.DataFrame()
        
        # Carrega pagamentos
        for key, (filename, cols) in arquivos_pagamento.items():
            file_path = os.path.join(pasta_mes, filename)
            if os.path.exists(file_path):
                dados[key] = self.ler_csv(file_path, cols)
            else:
                self.logger.warning(f"Arquivo não encontrado: {file_path}")
                dados[key] = pd.DataFrame()
        
        return dados

    def converter_todos_wab_txt_para_json(
        self, mes_ano: Optional[str] = None
    ) -> List[str]:
        """
        Converte todos os arquivos WAB TXT para JSON em uma pasta ou mês específico
        
        Args:
            mes_ano: String no formato "072025" (opcional, se None converte todos)
            
        Returns:
            Lista com caminhos dos arquivos JSON criados
        """
        arquivos_convertidos = []
        
        try:
            if mes_ano:
                # Converte apenas um mês específico
                pasta_mes = os.path.join(self.base_path, self._get_pasta_mes(mes_ano))
                txt_path = os.path.join(pasta_mes, f'faturamento_WAB_{mes_ano}.txt')
                
                if os.path.exists(txt_path):
                    json_path = self.converter_wab_txt_para_json(txt_path)
                    if json_path:
                        arquivos_convertidos.append(json_path)
            else:
                # Converte todos os arquivos TXT encontrados
                for root, dirs, files in os.walk(self.base_path):
                    for file in files:
                        if file.startswith('faturamento_WAB_') and file.endswith('.txt'):
                            txt_path = os.path.join(root, file)
                            json_path = self.converter_wab_txt_para_json(txt_path)
                            if json_path:
                                arquivos_convertidos.append(json_path)
            
            if arquivos_convertidos:
                self.logger.info(f"Convertidos {len(arquivos_convertidos)} arquivos WAB TXT para JSON")
            else:
                self.logger.warning("Nenhum arquivo WAB TXT encontrado para conversão")
                
        except Exception as e:
            self.logger.error(f"Erro na conversão em lote: {e}")
        
        return arquivos_convertidos

    def _get_pasta_mes(self, mes_ano: str) -> str:
        """Converte código do mês para nome da pasta"""
        meses = {
            '01': 'janeiro', '02': 'fevereiro', '03': 'marco', '04': 'abril',
            '05': 'maio', '06': 'junho', '07': 'julho', '08': 'agosto',
            '09': 'setembro', '10': 'outubro', '11': 'novembro', '12': 'dezembro'
        }
        mes = mes_ano[:2]
        return meses.get(mes, 'julho')  # Default para julho se não encontrar

    def padronizar_valores_monetarios(self, df: pd.DataFrame, colunas_valor: List[str]) -> pd.DataFrame:
        """Padroniza valores monetários removendo formatação"""
        df_copy = df.copy()
        
        for coluna in colunas_valor:
            if coluna in df_copy.columns:
                df_copy[coluna] = (df_copy[coluna]
                                  .astype(str)
                                  .str.replace('R$', '', regex=False)
                                  .str.replace('.', '', regex=False)
                                  .str.replace(',', '.', regex=False)
                                  .str.strip()
                                  .replace('', '0')
                                  .astype(float))
        
        return df_copy

    def padronizar_datas(self, df: pd.DataFrame, colunas_data: List[str]) -> pd.DataFrame:
        """Padroniza formato de datas"""
        df_copy = df.copy()
        
        for coluna in colunas_data:
            if coluna in df_copy.columns:
                df_copy[coluna] = pd.to_datetime(df_copy[coluna], format='%d/%m/%Y', errors='coerce')
        
        return df_copy
