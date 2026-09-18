import matplotlib.pyplot as plt

def exibir_tabelas_comparativas(resultados_cpu, resultados_memoria):
    """Exibe no terminal os dados organizados em tabelas."""
    print("\n" + "="*60)
    print("      Métricas — TABELA COMPARATIVA DE ESCALONAMENTO (CPU)")
    print("="*60)
    print(f"{'Algoritmo':<15} | {'Espera Média':<12} | {'Retorno Médio':<13} | {'Resposta Média':<14} | {'Trocas Contexto':<15}")
    print("-" * 78)
    for alg, m in resultados_cpu.items():
        print(f"{alg:<15} | {m['media_espera']:<12.2f} | {m['media_retorno']:<13.2f} | {m['media_resposta']:<14.2f} | {m['trocas_contexto']:<15}")

    print("\n" + "="*60)
    print("      Métricas — TABELA COMPARATIVA DE MEMÓRIA VIRTUAL")
    print("="*60)
    print(f"{'Algoritmo':<15} | {'Page Faults':<12} | {'Page Hits':<12} | {'Taxa de Faltas (%)':<18}")
    print("-" * 65)
    for alg, m in resultados_memoria.items():
        print(f"{alg:<15} | {m['page_faults']:<12} | {m['page_hits']:<12} | {m['taxa_faltas']:<18.2f}")

def gerar_graficos_comparativos(resultados_cpu, resultados_memoria):
    """Gera gráficos de barras comparando os algoritmos de CPU e Memória."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Gráfico 1: Tempos Médios de CPU
    algoritmos_cpu = list(resultados_cpu.keys())
    espera = [resultados_cpu[a]['media_espera'] for a in algoritmos_cpu]
    resposta = [resultados_cpu[a]['media_resposta'] for a in algoritmos_cpu]

    x = range(len(algoritmos_cpu))
    axes[0].bar([i - 0.2 for i in x], espera, width=0.4, label='Espera Média', color='skyblue')
    axes[0].bar([i + 0.2 for i in x], resposta, width=0.4, label='Resposta Média', color='coral')
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(algoritmos_cpu)
    axes[0].set_ylabel("Tempo (unidades)")
    axes[0].set_title("Comparativo de Desempenho da CPU")
    axes[0].legend()
    axes[0].grid(axis='y', linestyle='--', alpha=0.7)

    # Gráfico 2: Page Faults
    algoritmos_mem = list(resultados_memoria.keys())
    faults = [resultados_memoria[a]['page_faults'] for a in algoritmos_mem]

    axes[1].bar(algoritmos_mem, faults, color=['#e74c3c', '#3498db', '#2ecc71'])
    axes[1].set_ylabel("Quantidade de Faltas")
    axes[1].set_title("Page Faults por Algoritmo de Memória")
    axes[1].grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.show()