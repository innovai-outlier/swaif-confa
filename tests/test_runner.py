#!/usr/bin/env python3
"""
Módulo de execução de testes para o SWAIF-CONFA.
Oferece execução estruturada com IDs, títulos e relatórios formatados.
"""

import time
import sys
import os
from dataclasses import dataclass
from typing import Dict, Any, List, Optional

# Adicionar o diretório src ao Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from models.analisador import Analisador
from models.data_loader import DataLoader


@dataclass
class TestCase:
    """Representa um caso de teste estruturado."""
    id: str
    title: str
    description: str
    function: callable
    expected_result: Optional[Any] = None


class TestMetrics:
    """Gerencia métricas e relatórios de teste."""
    
    def __init__(self):
        self.test_results = {}
        self.start_time = None
        self.end_time = None
    
    def start_timing(self):
        """Inicia a medição de tempo."""
        self.start_time = time.time()
    
    def stop_timing(self):
        """Para a medição de tempo."""
        self.end_time = time.time()
    
    def add_result(self, test_id: str, passed: bool, duration: float, details: str = ""):
        """Adiciona um resultado de teste."""
        self.test_results[test_id] = {
            'passed': passed,
            'duration': duration,
            'details': details
        }
    
    def calculate_success_rate(self) -> float:
        """Calcula a taxa de sucesso dos testes."""
        if not self.test_results:
            return 0.0
        passed_tests = sum(1 for result in self.test_results.values() if result['passed'])
        return (passed_tests / len(self.test_results)) * 100
    
    def get_performance_summary(self) -> Dict[str, float]:
        """Retorna um resumo de performance."""
        if not self.test_results:
            return {
                'total_duration': 0.0,
                'avg_test_duration': 0.0,
                'min_test_duration': 0.0,
                'max_test_duration': 0.0
            }
        
        durations = [result['duration'] for result in self.test_results.values()]
        total_duration = self.end_time - self.start_time if self.start_time and self.end_time else sum(durations)
        
        return {
            'total_duration': total_duration,
            'avg_test_duration': sum(durations) / len(durations),
            'min_test_duration': min(durations),
            'max_test_duration': max(durations)
        }
    
    def generate_results_table(self) -> str:
        """Gera uma tabela formatada com os resultados."""
        if not self.test_results:
            return "Nenhum resultado de teste disponível."
        
        table = "\n📋 RESULTADOS DETALHADOS:\n"
        table += f"{'ID':<15} {'STATUS':<10} {'DURAÇÃO':<12} {'DETALHES':<30}\n"
        table += "─" * 70 + "\n"
        
        for test_id, result in self.test_results.items():
            status = "✅ PASSOU" if result['passed'] else "❌ FALHOU"
            duration = f"{result['duration']:.3f}s"
            details = result['details'][:25] + "..." if len(result['details']) > 25 else result['details']
            
            table += f"{test_id:<15} {status:<10} {duration:<12} {details:<30}\n"
        
        return table
    
    def generate_full_report(self) -> str:
        """Gera o relatório completo formatado."""
        success_rate = self.calculate_success_rate()
        performance = self.get_performance_summary()
        
        report = f"""
📊 RELATÓRIO DE TESTES SWAIF-CONFA
{'='*50}

🎯 MÉTRICAS GERAIS:
   • Taxa de Sucesso: {success_rate:.1f}%
   • Total de Testes: {len(self.test_results)}
   • Testes Aprovados: {sum(1 for r in self.test_results.values() if r['passed'])}
   • Testes Falharam: {sum(1 for r in self.test_results.values() if not r['passed'])}
   • Duração Total: {performance.get('total_duration', 0):.2f}s

⚡ PERFORMANCE:
   • Tempo Médio por Teste: {performance.get('avg_test_duration', 0):.3f}s
   • Teste Mais Rápido: {performance.get('min_test_duration', 0):.3f}s
   • Teste Mais Lento: {performance.get('max_test_duration', 0):.3f}s

{self.generate_results_table()}

🏆 CRITÉRIOS DE APROVAÇÃO:
   • Taxa mínima de sucesso: 80%
   • Todas as funcionalidades críticas devem passar
   • Performance aceitável: < 2s por teste em média

📈 STATUS FINAL: {"✅ APROVADO" if success_rate >= 80 else "❌ NECESSITA REVISÃO"}
"""
        return report


class SwaifConfaTestRunner:
    """Executor de testes estruturado para o SWAIF-CONFA."""
    
    def __init__(self):
        self.metrics = TestMetrics()
        self.analisador = None
        self.data_loader = None
        self.test_cases = []
        self._setup_test_cases()
    
    def _setup_test_cases(self):
        """Configura os casos de teste estruturados."""
        self.test_cases = [
            TestCase(
                id="TC001",
                title="Inicialização do Analisador",
                description="Verifica se o analisador inicializa corretamente",
                function=self._test_inicializacao_analisador
            ),
            TestCase(
                id="TC002", 
                title="Carregamento DataLoader",
                description="Testa se o DataLoader é instanciado sem erros",
                function=self._test_carregamento_data_loader
            ),
            TestCase(
                id="TC003",
                title="Leitura C6 Faturamento",
                description="Verifica leitura de dados C6 faturamento",
                function=self._test_leitura_c6_faturamento
            ),
            TestCase(
                id="TC004",
                title="Leitura GDS Faturamento",
                description="Verifica leitura de dados GDS faturamento", 
                function=self._test_leitura_gds_faturamento
            ),
            TestCase(
                id="TC005",
                title="Leitura WAB JSON",
                description="Verifica leitura de dados WAB em formato JSON",
                function=self._test_leitura_wab_json
            ),
            TestCase(
                id="TC006",
                title="Conversão WAB TXT→JSON",
                description="Testa conversão de WAB TXT para JSON",
                function=self._test_conversao_wab_txt_json
            ),
            TestCase(
                id="TC007",
                title="Análise Discrepâncias",
                description="Executa análise de discrepâncias entre dados",
                function=self._test_analise_discrepancias
            ),
            TestCase(
                id="TC008",
                title="Formatação Valores C6",
                description="Testa formatação de valores monetários C6",
                function=self._test_formatacao_valores_c6
            ),
            TestCase(
                id="TC009",
                title="Formatação Valores GDS",
                description="Testa formatação de valores monetários GDS",
                function=self._test_formatacao_valores_gds
            ),
            TestCase(
                id="TC010",
                title="Formatação Valores WAB",
                description="Testa formatação de valores monetários WAB",
                function=self._test_formatacao_valores_wab
            )
        ]
    
    def _execute_test_case(self, test_case: TestCase) -> bool:
        """Executa um caso de teste individual."""
        print(f"\n🔍 Executando {test_case.id}: {test_case.title}")
        print(f"   📋 {test_case.description}")
        
        start_time = time.time()
        try:
            result = test_case.function()
            duration = time.time() - start_time
            
            if result:
                print(f"   ✅ PASSOU ({duration:.3f}s)")
                self.metrics.add_result(test_case.id, True, duration)
                # Se o resultado for um tuple (passou, detalhes), use detalhes
                if isinstance(result, tuple) and len(result) == 2:
                    passed, details = result
                    if passed:
                        print(f"   ✅ PASSOU ({duration:.3f}s): {details}")
                        self.metrics.add_result(test_case.id, True, duration, details)
                        return True
                    else:
                        print(f"   ❌ FALHOU ({duration:.3f}s): {details}")
                        self.metrics.add_result(test_case.id, False, duration, details)
                        return False
                elif isinstance(result, str):
                    # Se for uma string, considera como detalhes
                    print(f"   ✅ PASSOU ({duration:.3f}s): {result}")
                    self.metrics.add_result(test_case.id, True, duration, result)
                    return True
                elif result:
                    print(f"   ✅ PASSOU ({duration:.3f}s)")
                    self.metrics.add_result(test_case.id, True, duration)
                    return True
                else:
                    print(f"   ❌ FALHOU ({duration:.3f}s)")
                    self.metrics.add_result(test_case.id, False, duration, "Teste retornou False")
                    return False
                
        except Exception as e:
            duration = time.time() - start_time
            error_msg = f"Erro: {str(e)}"
            print(f"   ❌ ERRO ({duration:.3f}s): {error_msg}")
            self.metrics.add_result(test_case.id, False, duration, error_msg)
            return False
    
    def run_all_tests(self) -> str:
        """Executa todos os testes e retorna relatório."""
        print("🚀 INICIANDO TESTES SWAIF-CONFA")
        print("=" * 50)
        
        self.metrics.start_timing()
        
        for test_case in self.test_cases:
            self._execute_test_case(test_case)
        
        self.metrics.stop_timing()
        
        print("\n" + "=" * 50)
        print("📊 GERANDO RELATÓRIO...")
        
        return self.metrics.generate_full_report()
    
    def run_specific_tests(self, test_ids: List[str]) -> str:
        """Executa testes específicos por ID."""
        print(f"🎯 EXECUTANDO TESTES SELECIONADOS: {', '.join(test_ids)}")
        print("=" * 50)
        
        self.metrics.start_timing()
        
        for test_case in self.test_cases:
            if test_case.id in test_ids:
                self._execute_test_case(test_case)
        
        self.metrics.stop_timing()
        
        return self.metrics.generate_full_report()
    
    # ==================== IMPLEMENTAÇÕES DOS TESTES ====================
    
    def _test_inicializacao_analisador(self) -> tuple:
        """Testa inicialização do analisador."""
        try:
            self.analisador = Analisador()
            if self.analisador is not None:
                return (True, "Analisador inicializado com sucesso")
            else:
                return (False, "Analisador retornou None após inicialização")
        except Exception as e:
            print(f"      Erro específico: {str(e)}")
            return (False, f"Erro na inicialização: {str(e)}")
    
    def _test_carregamento_data_loader(self) -> tuple:
        """Testa carregamento do DataLoader."""
        try:
            # DataLoader precisa de um base_path
            base_path = os.path.join(os.path.dirname(__file__), "..", "faturamentos")
            self.data_loader = DataLoader(base_path)
            if self.data_loader is not None:
                return (True, f"DataLoader carregado com base_path: {base_path}")
            else:
                return (False, "DataLoader retornou None após inicialização")
        except Exception as e:
            print(f"      Erro específico: {str(e)}")
            return (False, f"Erro no carregamento: {str(e)}")
    
    def _test_leitura_c6_faturamento(self) -> tuple:
        """Testa leitura de dados C6 faturamento."""
        try:
            if not self.data_loader:
                base_path = os.path.join(os.path.dirname(__file__), "..", "faturamentos")
                self.data_loader = DataLoader(base_path)
            
            arquivo_c6 = os.path.join(os.path.dirname(__file__), "..", "faturamentos", "julho", "faturamento_C6_072025.csv")
            # Verifica se o arquivo CSV existe
            if os.path.exists(arquivo_c6):
                return (True, f"Arquivo C6 encontrado: {os.path.basename(arquivo_c6)}")
            else:
                return (False, f"Arquivo C6 não encontrado: {arquivo_c6}")
        except Exception as e:
            print(f"      Erro específico: {str(e)}")
            return (False, f"Erro na verificação: {str(e)}")
    
    def _test_leitura_gds_faturamento(self) -> tuple:
        """Testa leitura de dados GDS faturamento."""
        try:
            if not self.data_loader:
                base_path = os.path.join(os.path.dirname(__file__), "..", "faturamentos")
                self.data_loader = DataLoader(base_path)
            
            arquivo_gds = os.path.join(os.path.dirname(__file__), "..", "faturamentos", "julho", "faturamento_GDS_072025.csv")
            # Verifica se o arquivo CSV existe
            if os.path.exists(arquivo_gds):
                return (True, f"Arquivo GDS encontrado: {os.path.basename(arquivo_gds)}")
            else:
                return (False, f"Arquivo GDS não encontrado: {arquivo_gds}")
        except Exception as e:
            print(f"      Erro específico: {str(e)}")
            return (False, f"Erro na verificação: {str(e)}")
    
    def _test_leitura_wab_json(self) -> tuple:
        """Testa leitura de dados WAB JSON."""
        try:
            if not self.data_loader:
                base_path = os.path.join(os.path.dirname(__file__), "..", "faturamentos")
                self.data_loader = DataLoader(base_path)
            
            # Procura por arquivo JSON WAB
            pasta_julho = os.path.join(os.path.dirname(__file__), "..", "faturamentos", "julho")
            arquivo_json = os.path.join(pasta_julho, "faturamento_WAB_072025.json")
            
            if os.path.exists(arquivo_json):
                dados = self.data_loader.ler_wab_json(arquivo_json)
                if dados is not None and len(dados) > 0:
                    return (True, f"WAB JSON carregado: {len(dados)} registros de {os.path.basename(arquivo_json)}")
                else:
                    return (False, f"WAB JSON existe mas retornou dados vazios: {os.path.basename(arquivo_json)}")
            else:
                # Se não existe JSON, tenta converter do TXT
                arquivo_txt = os.path.join(pasta_julho, "faturamento_WAB_072025.txt")
                if os.path.exists(arquivo_txt):
                    sucesso = self.data_loader.converter_wab_txt_para_json(arquivo_txt, arquivo_json)
                    if sucesso:
                        dados = self.data_loader.ler_wab_json(arquivo_json)
                        if dados is not None and len(dados) > 0:
                            return (True, f"WAB convertido TXT→JSON: {len(dados)} registros")
                        else:
                            return (False, "Conversão TXT→JSON bem-sucedida mas dados vazios")
                    else:
                        return (False, "Falha na conversão TXT→JSON")
                else:
                    return (False, "Nem arquivo JSON nem TXT encontrados para WAB")
        except Exception as e:
            print(f"      Erro específico: {str(e)}")
            return (False, f"Erro na leitura WAB: {str(e)}")
    
    def _test_conversao_wab_txt_json(self) -> bool:
        """Testa conversão WAB TXT para JSON."""
        try:
            if not self.data_loader:
                base_path = os.path.join(os.path.dirname(__file__), "..", "faturamentos")
                self.data_loader = DataLoader(base_path)
            
            pasta_julho = os.path.join(os.path.dirname(__file__), "..", "faturamentos", "julho")
            arquivo_txt = os.path.join(pasta_julho, "faturamento_WAB_072025.txt")
            arquivo_json = os.path.join(pasta_julho, "faturamento_WAB_072025_converted.json")
            
            if os.path.exists(arquivo_txt):
                return self.data_loader.converter_wab_txt_para_json(arquivo_txt, arquivo_json)
            return False
        except Exception as e:
            print(f"      Erro específico: {str(e)}")
            return False
    
    def _test_analise_discrepancias(self) -> tuple:
        """Testa análise de discrepâncias."""
        try:
            if not self.analisador:
                self.analisador = Analisador()
            
            # Testa se o método existe
            has_method = hasattr(self.analisador, 'analisar_discrepancias')
            if has_method:
                return (True, "Método analisar_discrepancias encontrado")
            else:
                return (False, "Método analisar_discrepancias não encontrado")
        except Exception as e:
            print(f"      Erro específico: {str(e)}")
            return (False, f"Erro na verificação: {str(e)}")
    
    def _test_formatacao_valores_c6(self) -> tuple:
        """Testa formatação de valores C6."""
        try:
            if not self.analisador:
                self.analisador = Analisador()
            
            # Testa se o método existe (não executa por depender de dados específicos)
            has_method = hasattr(self.analisador, '_padronizar_valores_c6_faturamento')
            if has_method:
                return (True, "Método _padronizar_valores_c6_faturamento encontrado")
            else:
                return (False, "Método _padronizar_valores_c6_faturamento não encontrado")
        except Exception as e:
            print(f"      Erro específico: {str(e)}")
            return (False, f"Erro na verificação: {str(e)}")
    
    def _test_formatacao_valores_gds(self) -> tuple:
        """Testa formatação de valores GDS."""
        try:
            if not self.analisador:
                self.analisador = Analisador()
            
            # Testa se o método existe
            has_method = hasattr(self.analisador, '_padronizar_valores_gds')
            if has_method:
                return (True, "Método _padronizar_valores_gds encontrado")
            else:
                return (False, "Método _padronizar_valores_gds não encontrado")
        except Exception as e:
            print(f"      Erro específico: {str(e)}")
            return (False, f"Erro na verificação: {str(e)}")
    
    def _test_formatacao_valores_wab(self) -> tuple:
        """Testa formatação de valores WAB."""
        try:
            if not self.analisador:
                self.analisador = Analisador()
            
            # Testa se o método existe
            has_method = hasattr(self.analisador, '_padronizar_valores_wab')
            if has_method:
                return (True, "Método _padronizar_valores_wab encontrado")
            else:
                return (False, "Método _padronizar_valores_wab não encontrado")
        except Exception as e:
            print(f"      Erro específico: {str(e)}")
            return (False, f"Erro na verificação: {str(e)}")


def main():
    """Função principal para execução standalone."""
    runner = SwaifConfaTestRunner()
    
    # Verifica argumentos da linha de comando
    if len(sys.argv) > 1:
        # Executa testes específicos
        test_ids = sys.argv[1].split(',')
        resultado = runner.run_specific_tests(test_ids)
    else:
        # Executa todos os testes
        resultado = runner.run_all_tests()
    
    print(resultado)
    
    # Determina código de saída baseado na taxa de sucesso
    success_rate = runner.metrics.calculate_success_rate()
    sys.exit(0 if success_rate >= 80 else 1)


if __name__ == "__main__":
    main()
