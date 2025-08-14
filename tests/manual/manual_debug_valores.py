#!/usr/bin/env python3
"""
Script de teste para debug de padronização de valores
"""
import os
import sys

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.models.analisador import AnalisadorConciliacao
from src.models.data_loader import DataLoader


def main():
    print("🔍 TESTE DE DEBUG - PADRONIZAÇÃO DE VALORES")
    print("=" * 80)
    
    # Inicializa componentes
    data_loader = DataLoader()
    analisador = AnalisadorConciliacao()
    
    mes_ano = "072025"
    
    # Testa C6
    print("\n🏦 TESTANDO C6...")
    try:
        df_c6 = data_loader.carregar_c6_faturamento(mes_ano)
        print(f"✅ C6 carregado: {len(df_c6)} registros")
        
        # Aplica padronização com debug
        df_c6_padronizado = analisador._padronizar_valores_c6_faturamento(df_c6)
        print("✅ C6 padronizado concluído")
        
    except Exception as e:
        print(f"❌ Erro no C6: {e}")
    
    # Testa GDS
    print("\n🏢 TESTANDO GDS...")
    try:
        df_gds = data_loader.carregar_gds_faturamento(mes_ano)
        print(f"✅ GDS carregado: {len(df_gds)} registros")
        
        # Aplica padronização com debug
        df_gds_padronizado = analisador._padronizar_valores_gds(df_gds)
        print("✅ GDS padronizado concluído")
        
    except Exception as e:
        print(f"❌ Erro no GDS: {e}")
    
    # Testa WAB
    print("\n🌐 TESTANDO WAB...")
    try:
        df_wab = data_loader.carregar_wab_faturamento(mes_ano)
        print(f"✅ WAB carregado: {len(df_wab)} registros")
        
        # Aplica padronização com debug
        df_wab_padronizado = analisador._padronizar_valores_wab(df_wab)
        print("✅ WAB padronizado concluído")
        
    except Exception as e:
        print(f"❌ Erro no WAB: {e}")
    
    print("\n✅ TESTE COMPLETO!")

if __name__ == "__main__":
    main()
