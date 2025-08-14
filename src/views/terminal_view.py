"""Terminal View - Interface estilo mainframe no terminal"""
import os
import sys

from typing import Dict, List

from src.models.analisador import ResultadoAnalise

def format_brl(value: float) -> str:
    try:
        x = float(value)
    except Exception:  # pylint: disable=broad-except
        x = 0.0
    s = f"{x:,.2f}"
    s = s.replace(",", "_").replace(".", ",").replace("_", ".")
    return s


def format_percent(value: float) -> str:
    return f"{value:.1f}".replace(".", ",")


def safe_pause(prompt: str = "\nPressione ENTER para continuar...") -> None:
    try:
        if sys.stdin is None or not sys.stdin.isatty():
            return
        input(prompt)
    except (EOFError, OSError):
        return
      
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

        if not resultados:
            print("Nenhum resultado de conciliação encontrado.")
            self._exibir_resumo_geral(resultados)
            safe_pause("\nPressione ENTER para continuar...")
            return

        faturamentos = [r for r in resultados if r.tipo_analise == 'faturamento']
        pagamentos = [r for r in resultados if r.tipo_analise == 'pagamento']

        if faturamentos:
            self._exibir_secao_faturamento(faturamentos)

        if pagamentos:
            self._exibir_secao_pagamento(pagamentos)

        self._exibir_resumo_geral(resultados)

        safe_pause("\nPressione ENTER para continuar...")
    
    def _exibir_secao_faturamento(self, resultados: List[ResultadoAnalise]):
        """Exibe seção de análise de faturamento"""
        print("📊 ANÁLISE DE FATURAMENTO")
        print("-" * 60)
        print()
        
        for resultado in resultados:
            fonte1, fonte2 = resultado.par_fontes
            
            print(f"🔄 {fonte1} x {fonte2}")
            print(
                f"   {fonte1}: R$ {format_brl(resultado.total_fonte_1):>15} "
                f"({resultado.registros_fonte_1:>4} registros)"
            )
            print(
                f"   {fonte2}: R$ {format_brl(resultado.total_fonte_2):>15} "
                f"({resultado.registros_fonte_2:>4} registros)"
            )
            print(
                f"   Diferença: R$ {format_brl(resultado.diferenca):>12} "
                f"({format_percent(resultado.percentual_diferenca)}%)"
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
            print(
                f"   {fonte1}: R$ {format_brl(resultado.total_fonte_1):>15} "
                f"({resultado.registros_fonte_1:>4} registros)"
            )
            print(
                f"   {fonte2}: R$ {format_brl(resultado.total_fonte_2):>15} "
                f"({resultado.registros_fonte_2:>4} registros)"
            )
            print(
                f"   Diferença: R$ {format_brl(resultado.diferenca):>12} "
                f"({format_percent(resultado.percentual_diferenca)}%)"
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
            print(f"\n🔸 {fonte}")
            if dados['registros'] > 0:
                print(f"   {dados['registros']} registros")
                colunas = ', '.join(dados['colunas'][:5])
                print(
                    f"   {len(dados['colunas'])} colunas: {colunas}{'...' if len(dados['colunas']) > 5 else ''}"
                )
            else:
                print("   ❌ Nenhum dado encontrado")
        
        safe_pause("\nPressione ENTER para continuar...")
    
    def exibir_detalhes_fonte(self, detalhes: Dict, fonte: str, mes_ano: str):
        """Exibe detalhes específicos de uma fonte"""
        self.limpar_tela()
        self.exibir_cabecalho()
        
        print(f"DETALHES DA FONTE: {fonte.upper()} - {self._formatar_mes_ano(mes_ano)}")
        print("=" * self.largura_tela)
        print()
        
        if 'erro' in detalhes:
            print(f"❌ {detalhes['erro']}")
            safe_pause("\nPressione ENTER para continuar...")
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
            print(
                f"   {tipo_total.upper()}: R$ {format_brl(detalhes['total_principal']):>20}"
            )
            print("=" * 53)
        
        print()
        
        # Estatísticas
        if detalhes['estatisticas']:
            print("📈 ESTATÍSTICAS")
            print("-" * 40)
            for coluna, stats in detalhes['estatisticas'].items():
                print(f"{coluna}:")
                print(f"   Total: R$ {format_brl(stats['total']):>12}")
                print(f"   Média: R$ {format_brl(stats['media']):>12}")
                print(
                    f"   Min/Max: R$ {format_brl(stats['minimo'])} / R$ {format_brl(stats['maximo'])}"
                )
                print()
        
        # Primeiros registros
        print("📋 PRIMEIROS REGISTROS")
        print("-" * 40)
        if detalhes['primeiros_registros']:
            for i, registro in enumerate(detalhes['primeiros_registros'][:3], 1):
                print(f"Registro {i}: {str(registro)[:80]}{'...' if len(str(registro)) > 80 else ''}")
        
        safe_pause("\nPressione ENTER para continuar...")
    
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
        safe_pause("Pressione ENTER para continuar...")
    
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
