"""
Script Principal para Executar Testes do SWAIF-CONFA
Execute este arquivo para rodar toda a suite de testes
"""
import sys
import os

# Adiciona o diretório de testes ao path
sys.path.insert(0, os.path.dirname(__file__))

from test_runner import run_tests

if __name__ == "__main__":
    print("🧪 Iniciando Testes do SWAIF-CONFA")
    print("=" * 50)
    
    # Executa todos os testes
    metrics = run_tests()
    
    # Resultado final
    if metrics._is_approved():
        print("\n🎉 SISTEMA APROVADO EM TODOS OS TESTES!")
        exit(0)
    else:
        print("\n⚠️  SISTEMA PRECISA DE MELHORIAS!")
        exit(1)
