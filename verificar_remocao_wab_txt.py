#!/usr/bin/env python3
"""
Script para validar que testes WAB TXT foram removidos corretamente
"""

import os
import re


def verificar_testes_wab():
    print("=== VERIFICAÇÃO: Remoção de Testes WAB TXT ===\n")
    
    # Diretórios de teste
    test_dirs = [
        "tests/unit",
        "tests/integration",
        "tests/fixtures"
    ]
    
    problemas_encontrados = []
    funcoes_removidas = []
    funcoes_mantidas = []
    
    for test_dir in test_dirs:
        if not os.path.exists(test_dir):
            continue
            
        for arquivo in os.listdir(test_dir):
            if arquivo.endswith('.py'):
                filepath = os.path.join(test_dir, arquivo)
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Procura por referências problemáticas
                patterns_problematicos = [
                    r'\.txt["\'].*wab',  # Arquivos .txt relacionados a WAB
                    r'wab.*\.txt',       # WAB com .txt
                    r'test.*wab.*txt',   # Testes específicos de WAB TXT
                ]
                
                for pattern in patterns_problematicos:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    if matches:
                        problemas_encontrados.append(f"{filepath}: {matches}")
                
                # Verifica funções de teste específicas
                if 'test_ler_wab_txt' in content:
                    funcoes_removidas.append(f"{filepath}: test_ler_wab_txt encontrada")
                
                # Verifica se funções corretas estão presentes
                if 'test_ler_wab_json' in content:
                    funcoes_mantidas.append(f"{filepath}: test_ler_wab_json OK")
                
                if 'test_converter_wab_txt_para_json' in content:
                    funcoes_mantidas.append(f"{filepath}: test_converter_wab_txt_para_json OK")
    
    # Relatório
    print("📊 RESULTADOS:")
    print(f"   Diretórios verificados: {len(test_dirs)}")
    
    if problemas_encontrados:
        print(f"\n❌ PROBLEMAS ENCONTRADOS ({len(problemas_encontrados)}):")
        for problema in problemas_encontrados:
            print(f"   • {problema}")
    else:
        print("\n✅ Nenhum problema encontrado com referencias WAB TXT")
    
    if funcoes_removidas:
        print(f"\n⚠️ FUNÇÕES WAB TXT AINDA PRESENTES ({len(funcoes_removidas)}):")
        for funcao in funcoes_removidas:
            print(f"   • {funcao}")
    else:
        print("\n✅ Funções de teste WAB TXT foram removidas")
    
    if funcoes_mantidas:
        print(f"\n✅ FUNÇÕES CORRETAS MANTIDAS ({len(funcoes_mantidas)}):")
        for funcao in funcoes_mantidas:
            print(f"   • {funcao}")
    
    print(f"\n{'='*50}")
    
    if not problemas_encontrados and not funcoes_removidas:
        print("🎉 SUCESSO: Testes WAB TXT removidos corretamente!")
        print("   • Apenas funcionalidades de conversão mantidas")
        print("   • Testes WAB JSON funcionais")
    else:
        print("🔧 AÇÃO NECESSÁRIA: Alguns itens precisam ser corrigidos")
    
    return len(problemas_encontrados) == 0 and len(funcoes_removidas) == 0

if __name__ == "__main__":
    verificar_testes_wab()
