"""
Controller Principal - Coordena a lógica de negócio
"""
import logging
from typing import Dict, List

import pandas as pd

from src.models.analisador import Analisador, ResultadoAnalise
from src.models.data_loader import DataLoader


class ConciliacaoController:
    """Controller principal para orquestrar a conciliação"""
    
    def __init__(self, base_path: str):
        self.data_loader = DataLoader(base_path)
        self.analisador = Analisador()
        self.logger = logging.getLogger(__name__)
        
        # Configuração do logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

    def executar_conciliacao(self, mes_ano: str) -> List[ResultadoAnalise]:
        """
        Executa conciliação completa para um mês
        
        Args:
            mes_ano: String no formato "072025"
            
        Returns:
            Lista com resultados de análise
        """
        self.logger.info(f"Iniciando conciliação para {mes_ano}")
        
        # 1. Carrega dados
        dados = self.data_loader.carregar_dados_mes(mes_ano)
        
        # 2. Verifica se os dados foram carregados
        self._verificar_dados_carregados(dados)
        
        # 3. Executa análises
        resultados = self.analisador.analisar_todos_pares(dados)
        
        self.logger.info(f"Conciliação concluída. {len(resultados)} análises realizadas.")
        
        return resultados

    def obter_resumo_dados(self, mes_ano: str) -> Dict[str, Dict]:
        """
        Obtém resumo dos dados carregados
        
        Args:
            mes_ano: String no formato "072025"
            
        Returns:
            Dict com informações resumidas
        """
        dados = self.data_loader.carregar_dados_mes(mes_ano)
        
        resumo = {}
        for fonte, df in dados.items():
            resumo[fonte] = {
                'registros': len(df),
                'colunas': list(df.columns) if not df.empty else [],
                'amostra': df.head(3).to_dict('records') if not df.empty else []
            }
        
        return resumo

    def _verificar_dados_carregados(self, dados: Dict[str, pd.DataFrame]) -> None:
        """Verifica e registra status dos dados carregados"""
        for fonte, df in dados.items():
            if df.empty:
                self.logger.warning(f"Nenhum dado carregado para {fonte}")
            else:
                self.logger.info(f"{fonte}: {len(df)} registros carregados")

    def obter_detalhes_fonte(self, mes_ano: str, fonte: str) -> Dict:
        """
        Obtém detalhes específicos de uma fonte
        
        Args:
            mes_ano: String no formato "072025"
            fonte: Nome da fonte (ex: 'faturamento_c6', 'pagamento_gds')
            
        Returns:
            Dict com detalhes da fonte
        """
        dados = self.data_loader.carregar_dados_mes(mes_ano)
        
        if fonte not in dados:
            return {'erro': f'Fonte {fonte} não encontrada'}
        
        df = dados[fonte]
        
        if df.empty:
            return {'erro': f'Nenhum dado encontrado para {fonte}'}
        
        # Calcula estatísticas básicas para colunas numéricas
        estatisticas = {}
        for coluna in df.columns:
            if df[coluna].dtype in ['int64', 'float64']:
                estatisticas[coluna] = {
                    'total': float(df[coluna].sum()),
                    'media': float(df[coluna].mean()),
                    'minimo': float(df[coluna].min()),
                    'maximo': float(df[coluna].max())
                }
        
        # Calcula total principal baseado no tipo de fonte
        total_principal = 0.0
        tipo_total = ""
        
        if 'faturamento' in fonte:
            # Para faturamento, busca coluna de valor faturado
            coluna_valor = None
            if 'valor_faturado' in df.columns:
                coluna_valor = 'valor_faturado'
            elif 'valor_venda' in df.columns:
                coluna_valor = 'valor_venda'
            elif 'valor' in df.columns:
                coluna_valor = 'valor'
            
            if coluna_valor and df[coluna_valor].dtype in ['int64', 'float64']:
                total_principal = float(df[coluna_valor].sum())
            tipo_total = "Valor Faturado"
            
        elif 'pagamento' in fonte:
            # Para pagamento, busca coluna de valor recebível
            coluna_valor = None
            if 'valor_recebivel' in df.columns:
                coluna_valor = 'valor_recebivel'
            elif 'valor_parcela' in df.columns:
                coluna_valor = 'valor_parcela'
            elif 'valor' in df.columns:
                coluna_valor = 'valor'
            
            if coluna_valor and df[coluna_valor].dtype in ['int64', 'float64']:
                total_principal = float(df[coluna_valor].sum())
            tipo_total = "Valor Recebível"
        
        return {
            'registros': len(df),
            'colunas': list(df.columns),
            'estatisticas': estatisticas,
            'total_principal': total_principal,
            'tipo_total': tipo_total,
            'primeiros_registros': df.head(5).to_dict('records'),
            'ultimos_registros': df.tail(5).to_dict('records')
        }
