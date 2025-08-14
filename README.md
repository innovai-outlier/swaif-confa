# SWAIF-CONFA - Sistema de Conciliação Financeira

## 🎯 Objetivo

Sistema de conciliação financeira que compara totais de faturamento e pagamento entre diferentes fontes de dados (C6, GDS e WAB) para identificar divergências e garantir a integridade dos dados financeiros.

## 🏗️ Arquitetura

O sistema utiliza arquitetura **MVC (Model-View-Controller)** com interface estilo mainframe no terminal:

```
src/
├── models/           # Camada de dados e lógica de negócio
│   ├── data_loader.py    # Carregamento e padronização dos dados
│   └── analisador.py     # Análise e comparação dos totais
├── views/            # Camada de apresentação
│   └── terminal_view.py  # Interface de terminal estilo mainframe
└── controllers/      # Camada de controle
    └── conciliacao_controller.py  # Coordenação da lógica
```

## 📊 Funcionalidades

### 1. **Análise de Faturamento**
Compara totais entre pares de fontes:
- **GDS x C6**: Sistema oficial vs. dados bancários
- **GDS x WAB**: Sistema oficial vs. relatórios WhatsApp
- **C6 x WAB**: Dados bancários vs. relatórios WhatsApp

### 2. **Análise de Pagamento**
Compara totais entre:
- **GDS x C6**: Sistema oficial vs. dados bancários

### 3. **Interface Mainframe**
- Menu principal navegável
- Relatórios formatados
- Indicadores visuais de status
- Processamento em tempo real

## 📁 Estrutura de Dados

### Arquivos Esperados (por mês):
```
faturamentos/
├── julho/
│   ├── faturamento_C6_072025.csv     # Faturamento banco C6
│   ├── faturamento_GDS_072025.csv    # Faturamento sistema GDS
│   ├── faturamento_WAB_072025.txt    # Faturamento relatórios WAB
│   ├── pagamento_C6_072025.csv       # Pagamentos banco C6
│   └── pagamento_GDS_072025.csv      # Pagamentos sistema GDS
```

### Formatos de Dados:

#### **C6 Faturamento** (CSV com `;`)
```
DT_VENDA;HR_VENDA;VAL_FAT;VAL_PARC;BANDEIRA;NUM_CARTAO;OPERACAO;PARCELAS;STATUS
```

#### **GDS Faturamento/Pagamento** (CSV com `;`)
```
R/D;Data de emissão;Data de vencimento;Data de baixa;Responsável;Paciente;Descrição;...
```

#### **WAB Faturamento** (TXT estruturado)
```
DATA: 01/07/2025
VALOR PAGO: R$700,00
NOME DO PACIENTE (FORNECEDOR): João Silva
...
```

#### **C6 Pagamento** (CSV com `;`)
```
Hora da venda;Data da venda;Data do recebível;Valor da venda;Valor da parcela;...
```

## 🚀 Como Usar

### 1. **Executar o Sistema**
```bash
python main.py
```

### 2. **Menu Principal**
- **1. Executar Conciliação**: Análise completa dos dados
- **2. Visualizar Resumo dos Dados**: Estatísticas gerais
- **3. Detalhes por Fonte**: Análise específica de uma fonte
- **4. Configurações**: Informações do sistema
- **0. Sair**: Encerrar aplicação

### 3. **Interpretação dos Resultados**

#### **Status de Conformidade:**
- ✅ **CONFERE**: Diferença < 1%
- ⚠️ **PEQUENA DIVERGÊNCIA**: 1% ≤ diferença < 5%  
- ❌ **GRANDE DIVERGÊNCIA**: Diferença ≥ 5%

#### **Exemplo de Saída:**
```
📊 ANÁLISE DE FATURAMENTO
─────────────────────────────────────────────────────────
🔄 GDS x C6
   GDS: R$      25.450,00 (  42 registros)
   C6:  R$      25.480,00 (  38 registros)
   Diferença: R$     30,00 ( 0.12%)
   Status: ✅ CONFERE

🔄 GDS x WAB  
   GDS: R$      25.450,00 (  42 registros)
   WAB: R$      24.950,00 (  40 registros)
   Diferença: R$    500,00 ( 1.96%)
   Status: ⚠️ PEQUENA DIVERGÊNCIA
```

## 🔧 Configuração

### **Requisitos:**
- Python 3.7+
- pandas
- openpyxl (se necessário para Excel)

### **Instalação:**
```bash
pip install pandas openpyxl
```

### **Estrutura de Pastas:**
O sistema espera a pasta `faturamentos/` na raiz do projeto com subpastas por mês.

## 📈 Melhorias Futuras

1. **Interface Web**: Migração para interface web responsiva
2. **Banco de Dados**: Persistência dos resultados históricos  
3. **APIs**: Integração automática com sistemas fonte
4. **Alertas**: Notificações automáticas para divergências
5. **Dashboards**: Visualizações interativas
6. **Auditoria**: Log detalhado de todas as operações

## 🧪 Teste Rápido

Para testar o carregamento do sistema:
```bash
python -c "from main import SwaifConfaApp; app = SwaifConfaApp(); print('✅ Sistema OK!')"
```

## 📋 Log de Mudanças

### **v2.0** - Reforma Completa
- ✅ Nova arquitetura MVC
- ✅ Interface estilo mainframe
- ✅ Foco em análise de totais por fonte
- ✅ Suporte a CSV para GDS e C6
- ✅ Mantida função ler_wab_txt para WAB
- ✅ Remoção de funcionalidades de conciliação detalhada
- ✅ Pares de análise simplificados e focados

### **v1.0** - Versão Original  
- Sistema de conciliação detalhada por registro
- Múltiplas estratégias de matching
- Exportação de relatórios Excel/CSV
