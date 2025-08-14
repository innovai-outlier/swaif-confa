"""
Data Loader - Modelo para carregamento e padronização dos dados
"""
import pandas as pd
import os
from typing import Dict, List, Tuple
from datetime import datetime
import logging

class DataLoader:
    """Classe responsável pelo carregamento e padronização dos dados de faturamento e pagamento"""
    
    def __init__(self, base_path: str):
        self.base_path = base_path
        self.logger = logging.getLogger(__name__)
        
        # Mapeamentos de colunas para padronização
        self.faturamento_c6_cols = {
            'DT_VENDA': 'data',
            'HR_VENDA': 'hora', 
            'VAL_FAT': 'valor_faturado',
            'VAL_PARC': 'valor_parcela',
            'BANDEIRA': 'bandeira',
            'NUM_CARTAO': 'num_cartao',
            'OPERACAO': 'operacao',
            'PARCELAS': 'parcelas',
            'STATUS': 'status'
        }
        
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
        
        self.pagamento_c6_cols = {
            'Hora da venda': 'hora_venda',
            'Data da venda': 'data_venda',
            'Data do recebível': 'data_recebivel',
            'Valor da venda': 'valor_venda',
            'Valor da parcela': 'valor_parcela',
            'Descontos': 'descontos',
            'Valor do recebível': 'valor_recebivel',
            'Bandeira do cartão': 'bandeira',
            'Número do cartão': 'num_cartao',
            'Tipo de operação': 'tipo_operacao',
            'Parcelas': 'parcelas',
            'Status do recebível': 'status',
            'Código da venda': 'codigo_venda',
            'Instituição Financeira': 'instituicao_financeira',
            'CNPJ Instituição Financeira': 'cnpj_instituicao'
        }
        
        self.pagamento_gds_cols = self.faturamento_gds_cols  # Mesma estrutura
        
        self.wab_cols = {
            'DATA': 'data',
            'VALOR PAGO': 'valor_pago',
            'VALOR TOTAL': 'valor_total',
            'DESCRIÇÃO': 'descricao',
            'MODO DE PAGAMTO': 'forma_pagamento',
            'NOME DO PACIENTE (FORNECEDOR)': 'paciente',
            'OBS': 'obs'
        }

    def ler_csv(self, file_path: str, column_mapping: Dict[str, str]) -> pd.DataFrame:
        """Lê arquivo CSV e aplica mapeamento de colunas"""
        try:
            df = pd.read_csv(file_path, sep=';', encoding='utf-8')
            
            # Remove espaços dos nomes das colunas
            df.columns = df.columns.str.strip()
            
            # Aplica mapeamento de colunas
            df = df.rename(columns=column_mapping)
            
            self.logger.info(f"Arquivo CSV lido com sucesso: {os.path.basename(file_path)} - {len(df)} registros")
            return df
            
        except Exception as e:
            self.logger.error(f"Erro ao ler CSV {file_path}: {e}")
            return pd.DataFrame()

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
        try:
            registros = []
            with open(file_path, encoding='utf-8') as f:
                bloco = {}
                for linha in f:
                    linha = linha.strip()
                    if not linha:
                        if bloco:
                            registros.append(bloco)
                            bloco = {}
                        continue
                    if ':' in linha:
                        chave, valor = linha.split(':', 1)
                        bloco[chave.strip()] = valor.strip()
                if bloco:
                    registros.append(bloco)
                    
            df = pd.DataFrame(registros)
            
            # Aplica mapeamento de colunas
            df = df.rename(columns=self.wab_cols)
            
            self.logger.info(f"Arquivo WAB TXT lido com sucesso: {os.path.basename(file_path)} - {len(df)} registros")
            return df
            
        except Exception as e:
            self.logger.error(f"Erro ao ler WAB TXT {file_path}: {e}")
            return pd.DataFrame()

    def ler_wab_json(self, file_path: str) -> pd.DataFrame:
        """
        Lê o arquivo WAB em formato JSON (formato oficial para análises)
        
        Args:
            file_path: Caminho para o arquivo JSON do WAB
            
        Returns:
            DataFrame padronizado com dados do WAB
        """
        try:
            import json
            
            with open(file_path, encoding='utf-8') as f:
                dados = json.load(f)
            
            df = pd.DataFrame(dados)
            
            # Aplica mapeamento de colunas
            df = df.rename(columns=self.wab_cols)
            
            self.logger.info(f"Arquivo WAB JSON lido com sucesso: {os.path.basename(file_path)} - {len(df)} registros")
            return df
            
        except Exception as e:
            self.logger.error(f"Erro ao ler WAB JSON {file_path}: {e}")
            return pd.DataFrame()

    def converter_wab_txt_para_json(self, txt_path: str, json_path: str = None) -> str:
        """
        Converte arquivo WAB TXT para JSON
        
        Args:
            txt_path: Caminho do arquivo TXT original
            json_path: Caminho do arquivo JSON de destino (opcional)
            
        Returns:
            Caminho do arquivo JSON criado
        """
        try:
            import json
            
            # Define caminho do JSON se não fornecido
            if json_path is None:
                json_path = txt_path.replace('.txt', '.json')
            
            # Lê o arquivo TXT
            registros = []
            with open(txt_path, encoding='utf-8') as f:
                bloco = {}
                for linha in f:
                    linha = linha.strip()
                    if not linha:
                        if bloco:
                            registros.append(bloco)
                            bloco = {}
                        continue
                    if ':' in linha:
                        chave, valor = linha.split(':', 1)
                        bloco[chave.strip()] = valor.strip()
                if bloco:
                    registros.append(bloco)
            
            # Salva como JSON
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(registros, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"Arquivo WAB convertido: {os.path.basename(txt_path)} -> {os.path.basename(json_path)} ({len(registros)} registros)")
            return json_path
            
        except Exception as e:
            self.logger.error(f"Erro ao converter WAB TXT para JSON: {e}")
            return None

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

    def converter_todos_wab_txt_para_json(self, mes_ano: str = None) -> List[str]:
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
