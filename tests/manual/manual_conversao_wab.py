#!/usr/bin/env python3
"""
Script para testar e demonstrar a conversão WAB TXT para JSON
"""

import os

from src.models.data_loader import DataLoader


def test_conversao_wab():
    print("=== TESTE DE CONVERSÃO WAB TXT PARA JSON ===\n")
    
    # Inicializa o DataLoader
    loader = DataLoader()
    
    # Testa conversão do arquivo específico
    txt_path = "faturamentos/julho/faturamento_WAB_072025.txt"
    json_path = "faturamentos/julho/faturamento_WAB_072025_convertido.json"
    
    print("1. CONVERSÃO INDIVIDUAL:")
    print(f"Convertendo: {txt_path}")
    
    resultado = loader.converter_wab_txt_para_json(txt_path, json_path)
    
    if resultado:
        print(f"✅ Sucesso: {resultado}")
        
        # Verifica se o arquivo foi criado
        if os.path.exists(resultado):
            print(f"📁 Arquivo criado: {os.path.getsize(resultado)} bytes")
        
        # Testa leitura do JSON criado
        print("\n2. TESTE DE LEITURA JSON:")
        df_json = loader.ler_wab_json(resultado)
        print(f"📊 Registros carregados: {len(df_json)}")
        
        if not df_json.empty:
            print("🔍 Primeiras colunas:")
            print(df_json.columns.tolist()[:5])
            print("🔍 Primeira linha:")
            print(df_json.iloc[0].to_dict() if len(df_json) > 0 else "Sem dados")
    else:
        print("❌ Falha na conversão")
    
    print("\n3. COMPARAÇÃO TXT vs JSON:")
    
    # Carrega TXT original
    df_txt = loader.ler_wab_txt(txt_path)
    print(f"📄 TXT: {len(df_txt)} registros")
    
    # Carrega JSON convertido
    if resultado and os.path.exists(resultado):
        df_json = loader.ler_wab_json(resultado)
        print(f"🔧 JSON: {len(df_json)} registros")
        
        if len(df_txt) == len(df_json):
            print("✅ Mesma quantidade de registros")
        else:
            print("⚠️ Quantidades diferentes!")
            
        # Compara valores específicos
        if not df_txt.empty and not df_json.empty:
            print("\n🔍 Comparação de valores:")
            print("TXT - Primeiro valor_pago:", df_txt['valor_pago'].iloc[0] if 'valor_pago' in df_txt.columns else "N/A")
            print("JSON - Primeiro valor_pago:", df_json['valor_pago'].iloc[0] if 'valor_pago' in df_json.columns else "N/A")
    
    print("\n4. TESTE DO CARREGADOR COMPLETO:")
    
    # Testa o carregamento através do método principal
    dados = loader.carregar_dados_mes("072025")
    
    if 'faturamento_wab' in dados:
        df_wab = dados['faturamento_wab']
        print(f"📈 WAB carregado via carregar_dados_mes: {len(df_wab)} registros")
        print(f"🎯 Fonte utilizada: {'JSON' if os.path.exists('faturamentos/julho/faturamento_WAB_072025.json') else 'TXT'}")
    else:
        print("❌ WAB não carregado")
    
    print("\n=== TESTE CONCLUÍDO ===")

if __name__ == "__main__":
    test_conversao_wab()
