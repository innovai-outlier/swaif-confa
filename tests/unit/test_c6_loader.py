import pandas as pd

from src.models.c6_loader import FATURAMENTO_C6_COLS, ler_csv


def test_ler_csv(tmp_path):
    csv_file = tmp_path / 'teste.csv'
    dados = pd.DataFrame({'DT_VENDA': ['01/07/2025'], 'HR_VENDA': ['10:00'], 'VAL_FAT': [100]})
    dados.to_csv(csv_file, sep=';', index=False)
    df = ler_csv(str(csv_file), FATURAMENTO_C6_COLS)
    assert 'data' in df.columns
    assert df.loc[0, 'data'] == '01/07/2025'
