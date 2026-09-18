import json
from metrics import Processo, calcular_metricas_globais
from schedulers import fcfs, sjf, round_robin, prioridade
from memory import fifo, lru, optimal
from visualization import exibir_tabelas_comparativas, gerar_graficos_comparativos

def carregar_processos():
    with open('data/processes.json', 'r', encoding='utf-8') as f:
        dados = json.load(f)
    return [Processo(**d) for d in dados]

def main():
    print("=== KERNEL LAB — SIMULAÇÃO COMPLETA ===\n")
    
    processos_base = carregar_processos()

    # --- 1. ESCALONAMENTO DE CPU ---
    # FCFS
    _, procs_fcfs, trocas_fcfs = fcfs(processos_base)
    metricas_fcfs = calcular_metricas_globais(procs_fcfs, trocas_fcfs)

    # SJF
    _, procs_sjf, trocas_sjf = sjf(processos_base)
    metricas_sjf = calcular_metricas_globais(procs_sjf, trocas_sjf)

    # Round Robin (Quantum = 3)
    _, procs_rr, trocas_rr = round_robin(processos_base, quantum=3)
    metricas_rr = calcular_metricas_globais(procs_rr, trocas_rr)

    # Prioridade
    _, procs_prio, trocas_prio = prioridade(processos_base)
    metricas_prioridade = calcular_metricas_globais(procs_prio, trocas_prio)

    # --- 2. GERENCIAMENTO DE MEMÓRIA ---
    ref_paginas = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5, 2, 1, 5, 3, 2]
    
    # FIFO
    faults_fifo, hits_fifo, taxa_fifo, _ = fifo(ref_paginas, num_frames=4)

    # LRU
    faults_lru, hits_lru, taxa_lru, _ = lru(ref_paginas, num_frames=4)

    # Optimal
    faults_opt, hits_opt, taxa_opt, _ = optimal(ref_paginas, num_frames=4)

    # --- 3. CONSOLIDAÇÃO DOS RESULTADOS (ETAPA 5) ---
    resultados_cpu = {
        "FCFS": metricas_fcfs,
        "SJF": metricas_sjf,
        "Round Robin": metricas_rr,
        "Prioridade": metricas_prioridade
    }

    resultados_memoria = {
        "FIFO": {"page_faults": faults_fifo, "page_hits": hits_fifo, "taxa_faltas": taxa_fifo},
        "LRU": {"page_faults": faults_lru, "page_hits": hits_lru, "taxa_faltas": taxa_lru},
        "Optimal": {"page_faults": faults_opt, "page_hits": hits_opt, "taxa_faltas": taxa_opt}
    }

    # Exibição
    exibir_tabelas_comparativas(resultados_cpu, resultados_memoria)
    gerar_graficos_comparativos(resultados_cpu, resultados_memoria)

if __name__ == "__main__":
    main()