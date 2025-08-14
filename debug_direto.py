#!/usr/bin/env python3
"""
Debug direto via carregamento de dados reais
"""
import os
import sys
import pandas as pd

# Adiciona o diretório raiz ao path
project_root = r"c:\Users\dmene\Documents\LIVHealth\TI\Projetos\swaif-confa"
sys.path.insert(0, project_root)

def debug_c6():
    print("🔍 DEBUG C6 - CARREGAMENTO E PROCESSAMENTO DIRETO")
    print("=" * 80)
    
    # Caminho do arquivo C6
    arquivo_c6 = os.path.join(project_root, "faturamentos", "julho", "faturamento_C6_072025.csv")
    
    if not os.path.exists(arquivo_c6):
        print(f"❌ Arquivo não encontrado: {arquivo_c6}")
        return
    
    print(f"📁 Carregando: {arquivo_c6}")
    
    try:
        # Carrega o arquivo CSV
        df = pd.read_csv(arquivo_c6, sep=';')
        print(f"✅ Arquivo carregado: {len(df)} registros, {len(df.columns)} colunas")
        
        # Mostra as colunas
        print(f"📋 Colunas: {list(df.columns)}")
        
        # Procura colunas de valor
        colunas_valor = []
        for col in df.columns:
            if any(palavra in col.lower() for palavra in ['valor', 'faturado', 'liquido', 'receita', 'val_fat', 'val_parc']):
                colunas_valor.append(col)
        
        print(f"💰 Colunas de valor identificadas: {colunas_valor}")
        
        # Para cada coluna de valor, mostra amostras
        for coluna in colunas_valor:
            if coluna in df.columns:
                print(f"\n🔍 ANÁLISE DA COLUNA: {coluna}")
                print(f"   📝 Tipo: {df[coluna].dtype}")
                print(f"   📊 Primeiros 5 valores:")
                for i, val in enumerate(df[coluna].head(5)):
                    print(f"      [{i}] {repr(val)} (tipo: {type(val).__name__})")
                
                # Processamento
                print(f"   🔄 Processando...")
                valores_processados = (df[coluna]
                                     .astype(str)
                                     .str.strip()
                                     .str.replace('R$', '', regex=False)
                                     .str.strip()
                                     .str.replace('.', '', regex=False)   # Remove pontos de milhar
                                     .str.replace(',', '.', regex=False)  # Vírgula vira ponto decimal
                                     .replace('', '0'))
                
                print(f"   📊 Após processamento (primeiros 5):")
                for i, val in enumerate(valores_processados.head(5)):
                    print(f"      [{i}] {repr(val)}")
                
                # Conversão para float
                try:
                    valores_float = valores_processados.astype(float)
                    total = valores_float.sum()
                    print(f"   💰 TOTAL: R$ {total:,.2f}")
                    print(f"   📈 Min: R$ {valores_float.min():.2f}, Max: R$ {valores_float.max():.2f}")
                    
                    # Verifica valores problemáticos
                    zeros = (valores_float == 0).sum()
                    nulos = valores_float.isna().sum()
                    if zeros > 0:
                        print(f"   ⚠️ Valores zerados: {zeros}")
                    if nulos > 0:
                        print(f"   ⚠️ Valores nulos: {nulos}")
                        
                except ValueError as e:
                    print(f"   ❌ Erro na conversão: {e}")
                    # Tenta conversão segura
                    valores_safe = pd.to_numeric(valores_processados, errors='coerce').fillna(0)
                    total_safe = valores_safe.sum()
                    print(f"   💰 TOTAL (conversão segura): R$ {total_safe:,.2f}")
        
        print(f"\n✅ DEBUG C6 CONCLUÍDO")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_c6()
