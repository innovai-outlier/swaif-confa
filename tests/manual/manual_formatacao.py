#!/usr/bin/env python3
"""
Script para testar a formatação de valores nas diferentes fontes
"""

import pandas as pd

from src.models.analisador import Analisador


def test_formatacao():
    print("=== TESTE DE FORMATAÇÃO POR FONTE ===\n")
    
    analisador = Analisador()
    
    # Teste C6 Faturamento - Formato: '; R$ 600,00 ;'
    print("1. C6 FATURAMENTO:")
    df_c6_fat = pd.DataFrame({
        'VAL_FAT': [' R$ 600,00 ', ' R$ 1200,50 ', ' R$ 35,75 '],
        'VAL_PARC': [' R$ 600,00 ', ' R$ 400,17 ', ' R$ 35,75 ']
    })
    print("Original C6:")
    print(df_c6_fat)
    result_c6_fat = analisador._padronizar_valores_c6_faturamento(df_c6_fat)
    print("Processado C6:")
    print(result_c6_fat)
    print()
    
    # Teste GDS - Formato: ';1200;' ou ';1173,48;'
    print("2. GDS:")
    df_gds = pd.DataFrame({
        'Valor': ['1200', '1173,48', '580,25'],
        'Valor líquido': ['1173,48', '1090,33', '568,04']
    })
    print("Original GDS:")
    print(df_gds)
    result_gds = analisador._padronizar_valores_gds(df_gds)
    print("Processado GDS:")
    print(result_gds)
    print()
    
    # Teste WAB - Formato: 'R$700,00'
    print("3. WAB:")
    df_wab = pd.DataFrame({
        'valor_pago': ['R$700,00', 'R$1500,50', 'R$300,25'],
        'valor_total': ['R$700,00', 'R$1500,50', 'R$300,25']
    })
    print("Original WAB:")
    print(df_wab)
    result_wab = analisador._padronizar_valores_wab(df_wab)
    print("Processado WAB:")
    print(result_wab)
    print()
    
    print("=== TESTE CONCLUÍDO ===")

if __name__ == "__main__":
    test_formatacao()
