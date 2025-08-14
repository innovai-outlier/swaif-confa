import logging
import os
from typing import Dict

import pandas as pd

logger = logging.getLogger(__name__)

FATURAMENTO_C6_COLS: Dict[str, str] = {
    'DT_VENDA': 'data',
    'HR_VENDA': 'hora',
    'VAL_FAT': 'valor_faturado',
    'VAL_PARC': 'valor_parcela',
    'BANDEIRA': 'bandeira',
    'NUM_CARTAO': 'num_cartao',
    'OPERACAO': 'operacao',
    'PARCELAS': 'parcelas',
    'STATUS': 'status',
}

PAGAMENTO_C6_COLS: Dict[str, str] = {
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
    'CNPJ Instituição Financeira': 'cnpj_instituicao',
}

def ler_csv(file_path: str, column_mapping: Dict[str, str]) -> pd.DataFrame:
    """Lê arquivo CSV e aplica mapeamento de colunas."""
    try:
        df = pd.read_csv(file_path, sep=';', encoding='utf-8')
        df.columns = df.columns.str.strip()
        df = df.rename(columns=column_mapping)
        logger.info(
            "Arquivo CSV lido com sucesso: %s - %d registros",
            os.path.basename(file_path),
            len(df),
        )
        return df
    except Exception as exc:  # pylint: disable=broad-except
        logger.error("Erro ao ler CSV %s: %s", file_path, exc)
        return pd.DataFrame()
