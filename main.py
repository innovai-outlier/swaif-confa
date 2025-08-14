"""
SWAIF-CONFA - Sistema de Conciliação Financeira
Aplicação principal com arquitetura MVC
"""
import os
import sys

# Adiciona o diretório raiz ao path para imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.controllers.conciliacao_controller import ConciliacaoController
from src.views.terminal_view import TerminalView


class SwaifConfaApp:
    """Aplicação principal do sistema"""
    
    def __init__(self):
        # Caminho base para os arquivos de dados
        base_path = os.path.join(os.path.dirname(__file__), "faturamentos")
        
        self.controller = ConciliacaoController(base_path)
        self.view = TerminalView()
        self.rodando = True
    
    def executar(self):
        """Loop principal da aplicação"""
        self.view.exibir_cabecalho()
        print("Sistema iniciado com sucesso!")
        print("Pressione ENTER para continuar...")
        input()
        
        while self.rodando:
            opcao = self.view.exibir_menu_principal()
            self._processar_opcao(opcao)
    
    def _processar_opcao(self, opcao: str):
        """Processa a opção escolhida pelo usuário"""
        if opcao == "1":
            self._executar_conciliacao()
        elif opcao == "2":
            self._visualizar_resumo_dados()
        elif opcao == "3":
            self._detalhar_fonte()
        elif opcao == "4":
            self._exibir_configuracoes()
        elif opcao == "0":
            self._sair()
        else:
            self.view.exibir_erro("Opção inválida! Escolha uma opção válida do menu.")
    
    def _executar_conciliacao(self):
        """Executa conciliação completa"""
        try:
            mes_ano = self.view.solicitar_mes_ano()
            
            self.view.exibir_processando("Executando conciliação...")
            
            resultados = self.controller.executar_conciliacao(mes_ano)
            
            if resultados:
                self.view.exibir_resultados_conciliacao(resultados, mes_ano)
            else:
                self.view.exibir_erro("Nenhum resultado de conciliação obtido. Verifique os dados.")
                
        except Exception as e:
            self.view.exibir_erro(f"Erro durante a conciliação: {str(e)}")
    
    def _visualizar_resumo_dados(self):
        """Visualiza resumo dos dados carregados"""
        try:
            mes_ano = self.view.solicitar_mes_ano()
            
            self.view.exibir_processando("Carregando resumo dos dados...")
            
            resumo = self.controller.obter_resumo_dados(mes_ano)
            
            self.view.exibir_resumo_dados(resumo, mes_ano)
            
        except Exception as e:
            self.view.exibir_erro(f"Erro ao obter resumo: {str(e)}")
    
    def _detalhar_fonte(self):
        """Exibe detalhes de uma fonte específica"""
        try:
            mes_ano = self.view.solicitar_mes_ano()
            fonte = self.view.solicitar_fonte()
            
            self.view.exibir_processando(f"Carregando detalhes de {fonte}...")
            
            detalhes = self.controller.obter_detalhes_fonte(mes_ano, fonte)
            
            self.view.exibir_detalhes_fonte(detalhes, fonte, mes_ano)
            
        except Exception as e:
            self.view.exibir_erro(f"Erro ao obter detalhes: {str(e)}")
    
    def _exibir_configuracoes(self):
        """Exibe configurações do sistema"""
        self.view.limpar_tela()
        self.view.exibir_cabecalho()
        
        print("⚙️  CONFIGURAÇÕES DO SISTEMA")
        print("=" * 60)
        print()
        print("📂 Diretório de dados:", self.controller.data_loader.base_path)
        print("📋 Pares de análise de faturamento: (GDS x C6), (GDS x WAB), (C6 x WAB)")
        print("📋 Pares de análise de pagamento: (GDS x C6)")
        print()
        print("🔧 ESTRUTURA DE ARQUIVOS ESPERADA:")
        print("   faturamentos/")
        print("   ├── julho/")
        print("   │   ├── faturamento_C6_072025.csv")
        print("   │   ├── faturamento_GDS_072025.csv")
        print("   │   ├── faturamento_WAB_072025.txt")
        print("   │   ├── pagamento_C6_072025.csv")
        print("   │   └── pagamento_GDS_072025.csv")
        print("   └── [outros meses...]")
        print()
        print("📊 TOLERÂNCIAS:")
        print("   ✅ Conforme: diferença < 1%")
        print("   ⚠️  Pequena divergência: 1% ≤ diferença < 5%")
        print("   ❌ Grande divergência: diferença ≥ 5%")
        
        input("\nPressione ENTER para voltar ao menu...")
    
    def _sair(self):
        """Encerra a aplicação"""
        self.view.limpar_tela()
        self.view.exibir_cabecalho()
        
        print("👋 Encerrando SWAIF-CONFA...")
        print("Obrigado por usar o sistema!")
        print()
        
        self.rodando = False

def main():
    """Função principal"""
    try:
        app = SwaifConfaApp()
        app.executar()
    except KeyboardInterrupt:
        print("\n\n👋 Sistema encerrado pelo usuário.")
    except Exception as e:
        print(f"\n❌ Erro crítico: {e}")
        print("O sistema será encerrado.")

if __name__ == "__main__":
    main()
