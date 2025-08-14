# 🧪 Sistema de Testes SWAIF-CONFA

Este diretório contém a suite completa de testes para o sistema SWAIF-CONFA de conciliação financeira.

## 📁 Estrutura

```
tests/
├── __init__.py                 # Inicialização do módulo de testes
├── test_runner.py             # Runner principal com métricas
├── run_all_tests.py          # Script para executar todos os testes
├── README.md                 # Esta documentação
├── unit/                     # Testes unitários
│   ├── test_data_loader.py   # Testes do carregador de dados
│   ├── test_analisador.py    # Testes do analisador
│   ├── test_controller.py    # Testes do controller
│   └── test_terminal_view.py # Testes da interface terminal
├── integration/              # Testes de integração
│   └── test_integration.py   # Testes de integração completa
└── fixtures/                 # Dados de teste
    └── test_data.py          # Gerador de dados de teste
```

## 🚀 Como Executar

### Execução Completa
```bash
# Executa todos os testes com relatório detalhado
python tests/run_all_tests.py

# Ou diretamente o runner
python tests/test_runner.py
```

### Execução Específica
```bash
# Apenas testes unitários
python -m unittest discover tests/unit

# Apenas testes de integração
python -m unittest discover tests/integration

# Teste específico
python -m unittest tests.unit.test_data_loader.TestDataLoader.test_init_data_loader
```

## 📊 Métricas de Aprovação

O sistema utiliza as seguintes métricas para determinar aprovação:

### ✅ Critérios de Sucesso:
- **Taxa de Sucesso**: ≥ 90% dos testes devem passar
- **Performance**: Execução total < 10 segundos
- **Cobertura**: Todos os componentes principais testados
  - Data Loader
  - Analisador
  - Controller
  - Terminal View
  - Integração

### 📈 Métricas Coletadas:
- Tempo de execução por teste
- Taxa de sucesso geral
- Detalhes de falhas
- Performance do sistema
- Cobertura de componentes

## 🧪 Tipos de Teste

### 1. Testes Unitários
Testam componentes individuais isoladamente:

- **Data Loader**: Carregamento de arquivos CSV/TXT
- **Analisador**: Padronização e cálculos de valores
- **Controller**: Coordenação entre componentes
- **Terminal View**: Interface de usuário

### 2. Testes de Integração
Testam interação entre componentes:

- Fluxo completo de conciliação
- Consistência de dados entre componentes
- Performance do sistema integrado
- Tratamento de erros

### 3. Testes de Performance
Verificam performance do sistema:

- Tempo de carregamento de dados
- Velocidade de processamento
- Uso de memória

## 🛠️ Fixtures de Teste

O sistema inclui fixtures para gerar dados de teste consistentes:

### Formatos de Dados Suportados

#### WAB (JSON - Formato Oficial)
- **Arquivo**: `faturamento_WAB_MMAAAA.json`
- **Estrutura**: Array de objetos JSON
- **Campos**: DATA, VALOR PAGO, VALOR TOTAL, DESCRIÇÃO, MODO DE PAGAMTO, NOME DO PACIENTE (FORNECEDOR), OBS
- **Uso**: Formato principal para todas as análises

#### WAB TXT (Legacy)
- **Status**: Mantido apenas para conversão/migração
- **Funcionalidade**: `converter_wab_txt_para_json()`
- **Uso**: Não usado para análises diretas

### Uso das Fixtures

```python
from tests.fixtures.test_data import TestDataFixtures, TestContextManager

# Uso básico
with TestContextManager('complete') as temp_dir:
    # Dados completos criados automaticamente (inclui WAB JSON)
    controller = ConciliacaoController(temp_dir)
    resultados = controller.executar_conciliacao('072025')

# Dados corrompidos para teste de robustez
with TestContextManager('corrupted') as temp_dir:
    # Testa tratamento de erros
    pass

# Dados mínimos
with TestContextManager('minimal') as temp_dir:
    # Ambiente de teste simples
    pass
```

## 📋 Relatórios

### Relatório Console
O sistema exibe em tempo real:
- ✅ Testes que passaram
- ❌ Testes que falharam
- ⚡ Métricas de performance
- 📊 Resumo final

### Relatório Arquivo
Gera arquivo `test_report_YYYYMMDD_HHMMSS.txt` com:
- Relatório completo detalhado
- Métricas de aprovação
- Detalhes de falhas
- Recomendações

## 🔍 Exemplo de Saída

```
🚀 Iniciando Suite de Testes SWAIF-CONFA
============================================================

🔬 Executando Testes Unitários...
  ✅ TestDataLoader.test_init_data_loader (0.002s)
  ✅ TestDataLoader.test_ler_csv_arquivo_valido (0.015s)
  ✅ TestAnalisador.test_padronizar_valores_c6_faturamento (0.008s)
  ...

🔗 Executando Testes de Integração...
  ✅ TestIntegracaoCompleta.test_fluxo_completo_conciliacao (0.234s)
  ✅ TestIntegracaoCompleta.test_performance_sistema_completo (0.189s)
  ...

⚡ Executando Testes de Performance...
  ✅ performance_data_loading (0.156s)
  ✅ performance_processing (0.287s)

📊 RELATÓRIO DE TESTES SWAIF-CONFA
==================================================

🎯 MÉTRICAS GERAIS:
   • Taxa de Sucesso: 96.2%
   • Total de Testes: 26
   • Testes Aprovados: 25
   • Testes Falharam: 1
   • Duração Total: 1.45s

⚡ PERFORMANCE:
   • Tempo Médio por Teste: 0.056s
   • Teste Mais Rápido: 0.001s
   • Teste Mais Lento: 0.287s

🏆 CRITÉRIOS DE APROVAÇÃO:
   • Taxa de Sucesso Mínima: 90% ✅
   • Performance Aceitável: <10s total ✅
   • Cobertura de Componentes: 100% ✅

🎉 SISTEMA APROVADO!
```

## 🐛 Debugging

Para debugar testes específicos:

```python
# Adicione em qualquer teste
import pdb; pdb.set_trace()

# Ou use logging
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🔧 Extensão

Para adicionar novos testes:

1. **Teste Unitário**: Crie arquivo em `tests/unit/`
2. **Teste Integração**: Adicione em `tests/integration/`
3. **Novos Dados**: Estenda `tests/fixtures/test_data.py`

### Exemplo de Novo Teste:
```python
import unittest
class TestNovaFuncionalidade(unittest.TestCase):
    def test_nova_feature(self):
        # Seu teste aqui
        self.assertTrue(True)
```

## 📞 Suporte

- Para problemas nos testes, verifique os logs detalhados
- Relatórios são salvos automaticamente para análise
- Use fixtures predefinidas para dados consistentes

---

**📝 Nota**: Este sistema de testes garante a qualidade e confiabilidade do SWAIF-CONFA através de validação automatizada abrangente.
