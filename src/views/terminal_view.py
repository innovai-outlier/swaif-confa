"""
Terminal View - Interface estilo mainframe no terminal
"""
import os
from typing import Dict, List

from src.models.analisador import ResultadoAnalise


class TerminalView:
    """Interface de terminal estilo mainframe"""
    
    def __init__(self):
        self.largura_tela = 120
        self.titulo_sistema = "SWAIF-CONFA - SISTEMA DE CONCILIAÇÃO FINANCEIRA"
        
    def limpar_tela(self):
        """Limpa a tela do terminal"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def exibir_cabecalho(self):
        """Exibe cabeçalho do sistema"""
        print("=" * self.largura_tela)
        print(f"{self.titulo_sistema:^{self.largura_tela}}")
        print("=" * self.largura_tela)
        print()
    
    def exibir_menu_principal(self) -> str:
        """
        Exibe menu principal e retorna opção escolhida
        
        Returns:
            String com a opção escolhida
        """
        self.limpar_tela()
        self.exibir_cabecalho()
        
        print("MENU PRINCIPAL")
        print("-" * 40)
        print("1. Executar Conciliação")
        print("2. Visualizar Resumo dos Dados")
        print("3. Detalhes por Fonte")
        print("4. Configurações")
        print("0. Sair")
        print()
        
        return input("Selecione uma opção: ").strip()
    
    def solicitar_mes_ano(self) -> str:
        """Solicita mês e ano para análise"""
        print("\nInforme o mês e ano para análise:")
        print("Formato: MMAAAA (ex: 072025 para julho/2025)")
        mes_ano = input("Mês/Ano: ").strip()
        
        # Validação básica
        if len(mes_ano) != 6 or not mes_ano.isdigit():
            print("⚠️  Formato inválido! Use MMAAAA (ex: 072025)")
            return self.solicitar_mes_ano()
        
        mes = int(mes_ano[:2])
        if mes < 1 or mes > 12:
            print("⚠️  Mês inválido! Use 01-12")
            return self.solicitar_mes_ano()
        
        return mes_ano
    
    def exibir_resultados_conciliacao(self, resultados: List[ResultadoAnalise], mes_ano: str):
        """Exibe resultados da conciliação"""
        self.limpar_tela()
        self.exibir_cabecalho()
        
        print(f"RESULTADOS DA CONCILIAÇÃO - {self._formatar_mes_ano(mes_ano)}")
        print("=" * self.largura_tela)
        print()
        
        # Separa resultados por tipo
        faturamentos = [r for r in resultados if r.tipo_analise == 'faturamento']
        pagamentos = [r for r in resultados if r.tipo_analise == 'pagamento']
        
        # Exibe faturamentos
        if faturamentos:
            self._exibir_secao_faturamento(faturamentos)
        
        # Exibe pagamentos
        if pagamentos:
            self._exibir_secao_pagamento(pagamentos)
        
        # Resumo geral
        self._exibir_resumo_geral(resultados)
        
        input("\nPressione ENTER para continuar...")
    
    def _exibir_secao_faturamento(self, resultados: List[ResultadoAnalise]):
        """Exibe seção de análise de faturamento"""
        print("📊 ANÁLISE DE FATURAMENTO")
        print("-" * 60)
        print()
        
        for resultado in resultados:
            fonte1, fonte2 = resultado.par_fontes
            
            print(f"🔄 {fonte1} x {fonte2}")
            print(f"   {fonte1}: R$ {resultado.total_fonte_1:>15,.2f} ({resultado.registros_fonte_1:>4} registros)")
            print(f"   {fonte2}: R$ {resultado.total_fonte_2:>15,.2f} ({resultado.registros_fonte_2:>4} registros)")
            print(
                f"   Diferença: R$ {resultado.diferenca:>12,.2f} ({resultado.percentual_diferenca:>6.2f}%)"
            )

            # Status da análise
            if abs(resultado.percentual_diferenca) < 1:
                status = "✅ CONFERE"
            elif abs(resultado.percentual_diferenca) < 5:
                status = "⚠️  PEQUENA DIVERGÊNCIA"
            else:
                status = "❌ GRANDE DIVERGÊNCIA"
            
            print(f"   Status: {status}")
            print()
        
        print("-" * 60)
        print()
    
    def _exibir_secao_pagamento(self, resultados: List[ResultadoAnalise]):
        """Exibe seção de análise de pagamento"""
        print("💰 ANÁLISE DE PAGAMENTO")
        print("-" * 60)
        print()
        
        for resultado in resultados:
            fonte1, fonte2 = resultado.par_fontes
            
            print(f"🔄 {fonte1} x {fonte2}")
            print(f"   {fonte1}: R$ {resultado.total_fonte_1:>15,.2f} ({resultado.registros_fonte_1:>4} registros)")
            print(f"   {fonte2}: R$ {resultado.total_fonte_2:>15,.2f} ({resultado.registros_fonte_2:>4} registros)")
            print(
                f"   Diferença: R$ {resultado.diferenca:>12,.2f} ({resultado.percentual_diferenca:>6.2f}%)"
            )

            # Status da análise
            if abs(resultado.percentual_diferenca) < 1:
                status = "✅ CONFERE"
            elif abs(resultado.percentual_diferenca) < 5:
                status = "⚠️  PEQUENA DIVERGÊNCIA"
            else:
                status = "❌ GRANDE DIVERGÊNCIA"
            
            print(f"   Status: {status}")
            print()
        
        print("-" * 60)
        print()
    
    def _exibir_resumo_geral(self, resultados: List[ResultadoAnalise]):
        """Exibe resumo geral das análises"""
        print("📋 RESUMO GERAL")
        print("-" * 40)
        
        total_divergencias = sum(1 for r in resultados if abs(r.percentual_diferenca) >= 1)
        total_analises = len(resultados)

        print(f"Total de análises realizadas: {total_analises}")
        print(f"Análises com divergência ≥1%: {total_divergencias}")
        taxa_conformidade = (
            (total_analises - total_divergencias) / total_analises * 100
            if total_analises
            else 0
        )
        print(f"Taxa de conformidade: {taxa_conformidade:.1f}%")
        
        if total_divergencias > 0:
            print(f"\n⚠️  Atenção: {total_divergencias} análise(s) com divergência!")
        else:
            print("\n✅ Todas as análises estão conformes!")
    
    def exibir_resumo_dados(self, resumo: Dict[str, Dict], mes_ano: str):
        """Exibe resumo dos dados carregados"""
        self.limpar_tela()
        self.exibir_cabecalho()
        
        print(f"RESUMO DOS DADOS - {self._formatar_mes_ano(mes_ano)}")
        print("=" * self.largura_tela)
        print()
        
        # Organiza por categoria
        faturamentos = {k: v for k, v in resumo.items() if 'faturamento' in k}
        pagamentos = {k: v for k, v in resumo.items() if 'pagamento' in k}
        
        if faturamentos:
            print("📊 FATURAMENTOS")
            print("-" * 50)
            for fonte, dados in faturamentos.items():
                fonte_limpa = fonte.replace('faturamento_', '').upper()
                print(f"   {fonte_limpa}: {dados['registros']:>6} registros")
            print()
        
        if pagamentos:
            print("💰 PAGAMENTOS")
            print("-" * 50)
            for fonte, dados in pagamentos.items():
                fonte_limpa = fonte.replace('pagamento_', '').upper()
                print(f"   {fonte_limpa}: {dados['registros']:>6} registros")
            print()
        
        print("📋 DETALHES TÉCNICOS")
        print("-" * 50)
        for fonte, dados in resumo.items():
            print(f"\n🔸 {fonte.upper()}")
            if dados['registros'] > 0:
                print(f"   Registros: {dados['registros']}")
                print(f"   Colunas: {', '.join(dados['colunas'][:5])}{'...' if len(dados['colunas']) > 5 else ''}")
            else:
                print("   ❌ Nenhum dado encontrado")
        
        input("\nPressione ENTER para continuar...")
    
    def exibir_detalhes_fonte(self, detalhes: Dict, fonte: str, mes_ano: str):
        """Exibe detalhes específicos de uma fonte"""
        self.limpar_tela()
        self.exibir_cabecalho()
        
        print(f"DETALHES DA FONTE: {fonte.upper()} - {self._formatar_mes_ano(mes_ano)}")
        print("=" * self.largura_tela)
        print()
        
        if 'erro' in detalhes:
            print(f"❌ {detalhes['erro']}")
            input("\nPressione ENTER para continuar...")
            return
        
        print("📊 INFORMAÇÕES GERAIS")
        print("-" * 40)
        print(f"Total de registros: {detalhes['registros']}")
        print(f"Total de colunas: {len(detalhes['colunas'])}")
        
        # Exibe total principal destacado
        if detalhes.get('total_principal', 0) > 0:
            tipo_total = detalhes.get('tipo_total', 'Total')
            print()
            print("💰" + "=" * 50)
            print(f"   {tipo_total.upper()}: R$ {detalhes['total_principal']:>20,.2f}")
            print("=" * 53)
        
        print()
        
        # Estatísticas
        if detalhes['estatisticas']:
            print("📈 ESTATÍSTICAS")
            print("-" * 40)
            for coluna, stats in detalhes['estatisticas'].items():
                print(f"{coluna}:")
                print(f"   Total: R$ {stats['total']:>12,.2f}")
                print(f"   Média: R$ {stats['media']:>12,.2f}")
                print(f"   Min/Max: R$ {stats['minimo']:.2f} / R$ {stats['maximo']:.2f}")
                print()
        
        # Primeiros registros
        print("📋 PRIMEIROS REGISTROS")
        print("-" * 40)
        if detalhes['primeiros_registros']:
            for i, registro in enumerate(detalhes['primeiros_registros'][:3], 1):
                print(f"Registro {i}: {str(registro)[:80]}{'...' if len(str(registro)) > 80 else ''}")
        
        input("\nPressione ENTER para continuar...")
    
    def solicitar_fonte(self) -> str:
        """Solicita qual fonte o usuário quer detalhar"""
        print("\nFontes disponíveis:")
        fontes = [
            "faturamento_c6", "faturamento_gds", "faturamento_wab",
            "pagamento_c6", "pagamento_gds"
        ]
        
        for i, fonte in enumerate(fontes, 1):
            print(f"{i}. {fonte}")
        
        try:
            opcao = int(input("\nEscolha uma fonte (número): ")) - 1
            if 0 <= opcao < len(fontes):
                return fontes[opcao]
            else:
                print("Opção inválida!")
                return self.solicitar_fonte()
        except ValueError:
            print("Por favor, digite um número!")
            return self.solicitar_fonte()
    
    def exibir_erro(self, mensagem: str):
        """Exibe mensagem de erro"""
        print(f"\n❌ ERRO: {mensagem}")
        input("Pressione ENTER para continuar...")
    
    def exibir_processando(self, mensagem: str = "Processando..."):
        """Exibe mensagem de processamento"""
        print(f"\n⏳ {mensagem}")
    
    def _formatar_mes_ano(self, mes_ano: str) -> str:
        """Formata mês/ano para exibição"""
        meses = {
            '01': 'Janeiro', '02': 'Fevereiro', '03': 'Março', '04': 'Abril',
            '05': 'Maio', '06': 'Junho', '07': 'Julho', '08': 'Agosto',
            '09': 'Setembro', '10': 'Outubro', '11': 'Novembro', '12': 'Dezembro'
        }
        
        mes = mes_ano[:2]
        ano = mes_ano[2:]
        
        return f"{meses.get(mes, mes)}/{ano}"
