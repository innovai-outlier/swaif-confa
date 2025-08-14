#!/usr/bin/env python3
"""
Debug completo do pipeline C6
"""
import os
import sys
import pandas as pd

# Adiciona o diretório raiz ao path
project_root = r"c:\Users\dmene\Documents\LIVHealth\TI\Projetos\swaif-confa"
sys.path.insert(0, project_root)

from src.models.data_loader import DataLoader
from src.models.analisador import Analisador

def debug_pipeline_c6():
    print("🔍 DEBUG COMPLETO - PIPELINE C6")
    print("=" * 80)
    
    # Inicializa componentes
    base_path = os.path.join(project_root, "faturamentos")
    data_loader = DataLoader(base_path)
    analisador = Analisador()
    
    mes_ano = "072025"
    
    print(f"📅 Mês/Ano: {mes_ano}")
    print(f"📁 Base path: {base_path}")
    
    try:
        print(f"\n🔄 ETAPA 1: Carregando dados via DataLoader...")
        dados = data_loader.carregar_dados_mes(mes_ano)
        
        print(f"✅ Dados carregados:")
        for fonte, df in dados.items():
            print(f"   {fonte}: {len(df)} registros")
        
        # Foco no C6 faturamento
        df_c6 = dados.get('faturamento_c6', pd.DataFrame())
        
        if df_c6.empty:
            print(f"❌ DataFrame C6 faturamento está vazio!")
            return
            
        print(f"\n🔍 ETAPA 2: Analisando DataFrame C6 carregado...")
        print(f"   📊 Shape: {df_c6.shape}")
        print(f"   📋 Colunas: {list(df_c6.columns)}")
        
        # Identifica colunas de valor
        colunas_valor = []
        for col in df_c6.columns:
            if any(palavra in col.lower() for palavra in ['valor', 'total', 'parcela', 'receita', 'val_fat', 'val_parc']):
                colunas_valor.append(col)
        
        print(f"   💰 Colunas de valor identificadas: {colunas_valor}")
        
        if not colunas_valor:
            print(f"   ❌ Nenhuma coluna de valor encontrada!")
            return
        
        # Mostra amostras
        for col in colunas_valor[:2]:  # Só as 2 primeiras
            print(f"\n   🔍 Coluna '{col}':")
            print(f"      Tipo: {df_c6[col].dtype}")
            print(f"      Sample: {df_c6[col].head(3).tolist()}")
        
        print(f"\n🔄 ETAPA 3: Aplicando padronização C6...")
        
        # Chama método do analisador
        df_c6_padronizado = analisador._padronizar_valores_c6_faturamento(df_c6)
        
        print(f"✅ Padronização concluída!")
        
        # Verifica resultados
        print(f"\n📊 ETAPA 4: Verificando resultados...")
        for col in colunas_valor[:2]:
            if col in df_c6_padronizado.columns:
                valores = df_c6_padronizado[col]
                total = valores.sum()
                print(f"   💰 {col}: R$ {total:,.2f}")
            else:
                print(f"   ❌ Coluna '{col}' não encontrada após padronização")
                
        print(f"\n✅ DEBUG PIPELINE CONCLUÍDO!")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_pipeline_c6()
