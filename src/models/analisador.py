"""Ferramentas de análise e comparação dos dados."""
import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

import pandas as pd


def _to_float_brl(value):
    """Convert strings like 'R$ 1.500,75' to float 1500.75."""
    if value is None:
        return 0.0
    if isinstance(value, (int, float)):
        return float(value)
    s = str(value).strip()
    if not s:
        return 0.0
    s = s.replace("R$", "").strip()
    s = s.replace(".", "").replace(",", ".")
    try:
        return float(s)
    except Exception:  # pylint: disable=broad-except
        return 0.0

@dataclass
class ResultadoAnalise:
    """Resultado da análise de um par de fontes."""
    par_fontes: Tuple[str, str]
    total_fonte_1: float
    total_fonte_2: float
    registros_fonte_1: int
    registros_fonte_2: int
    diferenca: float
    percentual_diferenca: float
    tipo_analise: str = "faturamento"  # "faturamento" ou "pagamento"
    detalhes_divergencias: List[Dict] = field(default_factory=list)

class Analisador:
    """Classe responsável pela análise e comparação dos totais entre fontes"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def analisar(self, dados: Dict[str, pd.DataFrame]) -> List[ResultadoAnalise]:
        """
        Método principal para análise - alias para analisar_todos_pares
        
        Args:
            dados: Dicionário com DataFrames das fontes
            
        Returns:
            Lista de ResultadoAnalise
        """
        return self.analisar_todos_pares(dados)
    
    def analisar_discrepancias(
        self, dados: Optional[Dict[str, pd.DataFrame]] = None
    ) -> List[ResultadoAnalise]:
        """
        Método para análise de discrepâncias - alias para analisar_todos_pares
        
        Args:
            dados: Dicionário com DataFrames das fontes (opcional)
            
        Returns:
            Lista de ResultadoAnalise
        """
        if dados is None:
            # Se não fornecer dados, retorna uma estrutura vazia para teste
            return []
        return self.analisar_todos_pares(dados)
    
    def calcular_totais_faturamento(self, dados: Dict[str, pd.DataFrame]) -> Dict[str, Dict]:
        """
        Calcula totais de faturamento por fonte
        
        Args:
            dados: Dict com DataFrames de cada fonte
            
        Returns:
            Dict com totais por fonte
        """
        totais: Dict[str, Dict] = {}

        # C6 Faturamento
        if 'faturamento_c6' in dados and not dados['faturamento_c6'].empty:
            df_c6 = dados['faturamento_c6'].copy()
            df_c6 = self._padronizar_valores_c6_faturamento(df_c6)

            # Usa coluna valor_faturado (principal do C6)
            if 'valor_faturado' in df_c6.columns:
                coluna_valor = 'valor_faturado'
            elif 'valor_venda' in df_c6.columns:
                coluna_valor = 'valor_venda'
            else:
                coluna_valor = 'valor'

            if coluna_valor in df_c6.columns:
                total_c6 = pd.to_numeric(df_c6[coluna_valor], errors="coerce").fillna(0).sum()
            else:
                total_c6 = 0.0

            totais['faturamento_c6'] = {
                'total': total_c6,
                'registros': len(df_c6),
            }
        else:
            totais['faturamento_c6'] = {'total': 0.0, 'registros': 0}

        # GDS Faturamento
        if 'faturamento_gds' in dados and not dados['faturamento_gds'].empty:
            df_gds = dados['faturamento_gds'].copy()
            df_gds = self._padronizar_valores_gds(df_gds)

            coluna_valor = 'valor' if 'valor' in df_gds.columns else 'valor_venda'
            if coluna_valor in df_gds.columns:
                total_gds = pd.to_numeric(df_gds[coluna_valor], errors="coerce").fillna(0).sum()
            else:
                total_gds = 0.0

            totais['faturamento_gds'] = {
                'total': total_gds,
                'registros': len(df_gds),
            }
        else:
            totais['faturamento_gds'] = {'total': 0.0, 'registros': 0}

        # WAB Faturamento
        if 'faturamento_wab' in dados and not dados['faturamento_wab'].empty:
            df_wab = dados['faturamento_wab'].copy()
            df_wab = self._padronizar_valores_wab(df_wab)

            coluna_valor = 'valor' if 'valor' in df_wab.columns else 'valor_venda'
            if coluna_valor in df_wab.columns:
                total_wab = pd.to_numeric(df_wab[coluna_valor], errors="coerce").fillna(0).sum()
            else:
                total_wab = 0.0

            totais['faturamento_wab'] = {
                'total': total_wab,
                'registros': len(df_wab),
            }
        else:
            totais['faturamento_wab'] = {'total': 0.0, 'registros': 0}

        return totais

    def calcular_totais_pagamento(self, dados: Dict[str, pd.DataFrame]) -> Dict[str, Dict]:
        """
        Calcula totais de pagamento por fonte
        
        Args:
            dados: Dict com DataFrames de cada fonte
            
        Returns:
            Dict com totais por fonte
        """
        totais: Dict[str, Dict] = {}

        # C6 Pagamento
        if 'pagamento_c6' in dados and not dados['pagamento_c6'].empty:
            df_c6 = dados['pagamento_c6'].copy()
            df_c6 = self._padronizar_valores_c6_pagamento(df_c6)
            # Filtra apenas recebidos se a coluna existir
            if 'status' in df_c6.columns:
                df_c6 = df_c6[df_c6['status'].str.contains('Recebido', na=False)]
            # Use a coluna de valor disponível
            valor_col = 'valor_recebivel' if 'valor_recebivel' in df_c6.columns else 'valor'
            total_c6 = pd.to_numeric(df_c6[valor_col], errors="coerce").fillna(0).sum()
            totais['pagamento_c6'] = {
                'total': total_c6,
                'registros': len(df_c6),
                'detalhes': df_c6.head(5).to_dict('records'),  # Limitado para performance
            }

        # GDS Pagamento
        if 'pagamento_gds' in dados and not dados['pagamento_gds'].empty:
            df_gds = dados['pagamento_gds'].copy()
            df_gds = self._padronizar_valores_gds(df_gds)
            # Filtra apenas receitas pagas se as colunas existirem
            if 'tipo' in df_gds.columns:
                df_gds = df_gds[df_gds['tipo'].str.contains('Receita', na=False)]
            if 'pago' in df_gds.columns:
                df_gds = df_gds[df_gds['pago'].str.contains('Sim', na=False)]
            # Use a coluna de valor disponível
            valor_col = 'valor_liquido' if 'valor_liquido' in df_gds.columns else 'valor'
            total_gds = pd.to_numeric(df_gds[valor_col], errors="coerce").fillna(0).sum()
            totais['pagamento_gds'] = {
                'total': total_gds,
                'registros': len(df_gds),
                'detalhes': df_gds.head(5).to_dict('records'),
            }

        return totais

    def analisar_par_faturamento(
        self, fonte1: str, fonte2: str, totais: Dict[str, Dict]
    ) -> ResultadoAnalise:
        """Analisa um par de fontes para faturamento"""
        total1 = totais.get(fonte1, {}).get('total', 0)
        total2 = totais.get(fonte2, {}).get('total', 0)
        registros1 = totais.get(fonte1, {}).get('registros', 0)
        registros2 = totais.get(fonte2, {}).get('registros', 0)
        
        diferenca = total1 - total2
        if total1 == 0 or total2 == 0 or max(total1, total2) <= 0:
            percentual_diferenca = 0.0
        else:
            percentual_diferenca = (diferenca / max(total1, total2)) * 100

        # Identifica divergências (implementar lógica detalhada se necessário)
        detalhes_divergencias: List[Dict] = []

        return ResultadoAnalise(
            par_fontes=(fonte1, fonte2),
            tipo_analise="faturamento",
            total_fonte_1=total1,
            total_fonte_2=total2,
            diferenca=diferenca,
            percentual_diferenca=percentual_diferenca,
            registros_fonte_1=registros1,
            registros_fonte_2=registros2,
            detalhes_divergencias=detalhes_divergencias,
        )

    def analisar_par_pagamento(
        self, fonte1: str, fonte2: str, totais: Dict[str, Dict]
    ) -> ResultadoAnalise:
        """Analisa um par de fontes para pagamento"""
        total1 = totais.get(fonte1, {}).get('total', 0)
        total2 = totais.get(fonte2, {}).get('total', 0)
        registros1 = totais.get(fonte1, {}).get('registros', 0)
        registros2 = totais.get(fonte2, {}).get('registros', 0)
        
        diferenca = total1 - total2
        if total1 == 0 or total2 == 0 or max(total1, total2) <= 0:
            percentual_diferenca = 0.0
        else:
            percentual_diferenca = (diferenca / max(total1, total2)) * 100

        detalhes_divergencias: List[Dict] = []

        return ResultadoAnalise(
            par_fontes=(fonte1, fonte2),
            tipo_analise="pagamento",
            total_fonte_1=total1,
            total_fonte_2=total2,
            diferenca=diferenca,
            percentual_diferenca=percentual_diferenca,
            registros_fonte_1=registros1,
            registros_fonte_2=registros2,
            detalhes_divergencias=detalhes_divergencias,
        )

    def analisar_todos_pares(self, dados: Dict[str, pd.DataFrame]) -> List[ResultadoAnalise]:
        """
        Executa análise completa de todos os pares definidos
        
        Returns:
            Lista com todos os resultados de análise
        """
        resultados = []
        
        # Calcula totais
        totais_faturamento = self.calcular_totais_faturamento(dados)
        totais_pagamento = self.calcular_totais_pagamento(dados)
        
        # Pares de análise de faturamento
        pares_faturamento = [
            ('faturamento_c6', 'faturamento_gds'),
            ('faturamento_c6', 'faturamento_wab'),
            ('faturamento_gds', 'faturamento_wab'),
        ]
        
        for fonte1, fonte2 in pares_faturamento:
            resultado = self.analisar_par_faturamento(fonte1, fonte2, totais_faturamento)
            resultados.append(resultado)
        
        # Pares de análise de pagamento
        pares_pagamento = [('pagamento_c6', 'pagamento_gds')]
        
        for fonte1, fonte2 in pares_pagamento:
            resultado = self.analisar_par_pagamento(fonte1, fonte2, totais_pagamento)
            resultados.append(resultado)
        
        return resultados

    def _comparar_fontes(self, par_fontes: Tuple[str, str], fonte1_dados: Dict, fonte2_dados: Dict) -> ResultadoAnalise:
        """
        Compara duas fontes e retorna resultado da análise
        
        Args:
            par_fontes: Tupla com nomes das fontes
            fonte1_dados: Dados da primeira fonte {'total': float, 'registros': int}
            fonte2_dados: Dados da segunda fonte {'total': float, 'registros': int}
            
        Returns:
            ResultadoAnalise com comparação
        """
        total1 = fonte1_dados.get('total', 0.0)
        total2 = fonte2_dados.get('total', 0.0)
        registros1 = fonte1_dados.get('registros', 0)
        registros2 = fonte2_dados.get('registros', 0)

        diferenca = abs(total1 - total2)

        base = max(total1, total2)
        if base <= 0 or total1 == 0.0 or total2 == 0.0:
            percentual_diferenca = 0.0
        else:
            percentual_diferenca = (diferenca / base) * 100.0

        return ResultadoAnalise(
            par_fontes=par_fontes,
            total_fonte_1=total1,
            total_fonte_2=total2,
            registros_fonte_1=registros1,
            registros_fonte_2=registros2,
            diferenca=diferenca,
            percentual_diferenca=percentual_diferenca,
        )

    def _padronizar_valores_c6_faturamento(self, df: pd.DataFrame) -> pd.DataFrame:
        """Padroniza valores monetários do C6 faturamento - Formato: '; R$ 600,00 ;'"""
        df_copy = df.copy()
        
        # Identifica colunas de valor de forma mais flexível
        colunas_valor = []
        for col in df_copy.columns:
            if any(palavra in col.lower() for palavra in ['valor', 'total', 'parcela', 'receita', 'val_fat', 'val_parc']):
                colunas_valor.append(col)
        
        # Se não encontrou nenhuma, usa padrões conhecidos
        if not colunas_valor:
            colunas_valor = ['valor_faturado', 'valor_parcela', 'valor', 'total']
        
        for coluna in colunas_valor:
            if coluna in df_copy.columns:
                # Tratamento específico para formato C6: '; R$ 600,00 ;'
                df_processed = (df_copy[coluna]
                              .astype(str)
                              .str.strip()                    # Remove espaços externos
                              .str.replace('R$', '', regex=False)  # Remove R$
                              .str.strip()                    # Remove espaços restantes
                              .str.replace('.', '', regex=False)   # Remove pontos de milhar
                              .str.replace(',', '.', regex=False)  # Vírgula vira ponto decimal
                              .str.strip()                    # Limpeza final
                              .replace('', '0'))
                
                # Converte para float com tratamento de erro
                try:
                    df_copy[coluna] = df_processed.astype(float)
                    print(f"   ✅ {coluna}: R$ {df_copy[coluna].sum():,.2f}")
                        
                except ValueError as e:
                    self.logger.warning(f"Erro ao converter coluna C6 {coluna}: {e}")
                    # Em caso de erro, usa conversão segura
                    df_copy[coluna] = pd.to_numeric(df_processed, errors='coerce').fillna(0)
                    print(f"   ⚠️ {coluna} (conversão segura): R$ {df_copy[coluna].sum():,.2f}")
                print("-" * 60)
        
        # Padroniza datas
        for col in df_copy.columns:
            if 'data' in col.lower():
                df_copy[col] = pd.to_datetime(df_copy[col], format='%d/%m/%Y', errors='coerce')
        
        return df_copy

    def _padronizar_valores_c6_pagamento(self, df: pd.DataFrame) -> pd.DataFrame:
        """Padroniza valores monetários do C6 pagamento - Formato similar ao faturamento"""
        df_copy = df.copy()
        
        # Identifica colunas de valor de forma mais flexível
        colunas_valor = []
        for col in df_copy.columns:
            if any(palavra in col.lower() for palavra in ['valor', 'total', 'parcela', 'receita', 'recebivel', 'desconto']):
                colunas_valor.append(col)
        
        # Se não encontrou nenhuma, usa padrões conhecidos  
        if not colunas_valor:
            colunas_valor = ['valor_venda', 'valor_parcela', 'valor_recebivel', 'descontos']
        
        for coluna in colunas_valor:
            if coluna in df_copy.columns:
                # Tratamento específico para valores C6 com possíveis negativos
                valores_tratados = []
                for valor in df_copy[coluna]:
                    valor_str = str(valor).strip()
                    
                    # Trata valores negativos como -R$ 26,52
                    if valor_str.startswith('-R$'):
                        valor_str = '-' + valor_str[3:].strip()  # Remove -R$ e mantém o -, remove espaços
                    elif valor_str.startswith('R$'):
                        valor_str = valor_str[2:].strip()  # Remove R$ e espaços
                    elif valor_str == '-':
                        valor_str = '0'  # Hífen sozinho vira 0
                    elif valor_str == '':
                        valor_str = '0'  # Vazio vira 0
                    
                    # Remove pontos de milhar e converte vírgula para ponto
                    valor_str = (valor_str
                                .replace('.', '')  # Remove pontos de milhar
                                .replace(',', '.'))  # Vírgula vira ponto decimal
                    
                    # Tenta converter para float
                    try:
                        valor_float = float(valor_str)
                        valores_tratados.append(valor_float)
                    except ValueError:
                        self.logger.warning(f"Valor problemático na coluna {coluna}: '{valor}' -> '{valor_str}'")
                        valores_tratados.append(0.0)
                
                df_copy[coluna] = valores_tratados
        
        # Padroniza datas
        for coluna_data in ['data_venda', 'data_recebivel']:
            if coluna_data in df_copy.columns:
                df_copy[coluna_data] = pd.to_datetime(df_copy[coluna_data], format='%d/%m/%Y', errors='coerce')
        
        return df_copy

    def _padronizar_valores_gds(self, df: pd.DataFrame) -> pd.DataFrame:
        """Padroniza valores monetários do GDS."""
        df_copy = df.copy()

        colunas_valor = [
            col
            for col in df_copy.columns
            if any(p in col.lower() for p in ['valor', 'total', 'liquido', 'receita'])
        ]
        if not colunas_valor:
            colunas_valor = ['valor', 'valor_liquido']

        for coluna in colunas_valor:
            if coluna in df_copy.columns:
                df_copy[coluna] = df_copy[coluna].map(_to_float_brl)

        for coluna_data in ['data_emissao', 'data_vencimento', 'data_baixa']:
            if coluna_data in df_copy.columns:
                df_copy[coluna_data] = pd.to_datetime(
                    df_copy[coluna_data], format='%d/%m/%Y', errors='coerce'
                )

        return df_copy

    def _padronizar_valores_wab(self, df: pd.DataFrame) -> pd.DataFrame:
        """Padroniza valores monetários do WAB."""
        df_copy = df.copy()

        colunas_valor = [
            col for col in df_copy.columns if any(p in col.lower() for p in ['valor', 'total', 'pago'])
        ]
        if not colunas_valor:
            colunas_valor = ['valor_pago', 'valor_total']

        for coluna in colunas_valor:
            if coluna in df_copy.columns:
                df_copy[coluna] = pd.to_numeric(df_copy[coluna], errors='coerce').fillna(0)

        if 'data' in df_copy.columns:
            df_copy['data'] = pd.to_datetime(df_copy['data'], format='%d/%m/%Y', errors='coerce')

        return df_copy
