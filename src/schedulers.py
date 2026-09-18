import copy
from collections import deque

# 1. FCFS
def fcfs(processos_in):
    processos = copy.deepcopy(processos_in)
    processos.sort(key=lambda p: p.chegada)
    
    tempo = 0
    gantt = []
    trocas_contexto = 0
    ultimo_proc = None

    for p in processos:
        if tempo < p.chegada:
            for t in range(tempo, p.chegada):
                gantt.append((t, "IDLE"))
            tempo = p.chegada

        if ultimo_proc is not None and ultimo_proc != p.id:
            trocas_contexto += 1
        ultimo_proc = p.id

        p.tempo_resposta = tempo - p.chegada
        p.tempo_espera = tempo - p.chegada
        
        for _ in range(p.burst_original):
            gantt.append((tempo, p.id))
            tempo += 1

        p.tempo_fim = tempo
        p.tempo_retorno = p.tempo_fim - p.chegada

    return gantt, processos, trocas_contexto


# 2. SJF (Não Preemptivo)
def sjf(processos_in):
    processos = copy.deepcopy(processos_in)
    tempo = 0
    gantt = []
    trocas_contexto = 0
    concluidos = 0
    n = len(processos)
    ultimo_proc = None

    while concluidos < n:
        # Processos prontos que já chegaram
        prontos = [p for p in processos if p.chegada <= tempo and p.burst_restante > 0]

        if prontos:
            # Seleciona o de menor burst
            p = min(prontos, key=lambda x: x.burst_original)
            
            if ultimo_proc is not None and ultimo_proc != p.id:
                trocas_contexto += 1
            ultimo_proc = p.id

            p.tempo_resposta = tempo - p.chegada
            p.tempo_espera = tempo - p.chegada

            for _ in range(p.burst_original):
                gantt.append((tempo, p.id))
                tempo += 1

            p.tempo_fim = tempo
            p.tempo_retorno = p.tempo_fim - p.chegada
            p.burst_restante = 0
            concluidos += 1
        else:
            gantt.append((tempo, "IDLE"))
            tempo += 1

    return gantt, processos, trocas_contexto


# 3. Prioridade (Não Preemptivo - Menor número = Maior prioridade)
def prioridade(processos_in):
    processos = copy.deepcopy(processos_in)
    tempo = 0
    gantt = []
    trocas_contexto = 0
    concluidos = 0
    n = len(processos)
    ultimo_proc = None

    while concluidos < n:
        prontos = [p for p in processos if p.chegada <= tempo and p.burst_restante > 0]

        if prontos:
            # Seleciona o de menor valor no campo prioridade
            p = min(prontos, key=lambda x: x.prioridade)

            if ultimo_proc is not None and ultimo_proc != p.id:
                trocas_contexto += 1
            ultimo_proc = p.id

            p.tempo_resposta = tempo - p.chegada
            p.tempo_espera = tempo - p.chegada

            for _ in range(p.burst_original):
                gantt.append((tempo, p.id))
                tempo += 1

            p.tempo_fim = tempo
            p.tempo_retorno = p.tempo_fim - p.chegada
            p.burst_restante = 0
            concluidos += 1
        else:
            gantt.append((tempo, "IDLE"))
            tempo += 1

    return gantt, processos, trocas_contexto


def round_robin(processos_in, quantum=3):
    processos = copy.deepcopy(processos_in)
    tempo = 0
    gantt = []
    fila = deque()
    trocas_contexto = 0
    proc_atual = None
    tempo_quantum = 0
    concluidos = 0
    n = len(processos)

    processos.sort(key=lambda p: p.chegada)

    while concluidos < n:
        # Adiciona processos que chegaram no tempo atual
        for p in processos:
            if p.chegada == tempo and p.burst_restante > 0 and p not in fila and p != proc_atual:
                fila.append(p)

        # Seleciona proximo processo da fila se a CPU estiver livre
        if proc_atual is None and fila:
            proc_atual = fila.popleft()
            if proc_atual.tempo_resposta is None:
                proc_atual.tempo_resposta = tempo - proc_atual.chegada

        if proc_atual:
            gantt.append((tempo, proc_atual.id))
            proc_atual.burst_restante -= 1
            tempo_quantum += 1

            # Processo finalizado
            if proc_atual.burst_restante == 0:
                proc_atual.tempo_fim = tempo + 1
                proc_atual.tempo_retorno = proc_atual.tempo_fim - proc_atual.chegada
                proc_atual.tempo_espera = proc_atual.tempo_retorno - proc_atual.burst_original
                proc_atual = None
                tempo_quantum = 0
                concluidos += 1
            # Quantum esgotado
            elif tempo_quantum == quantum:
                # Checa se chegaram novos processos antes de re-enfileirar o atual
                for p in processos:
                    if p.chegada == tempo + 1 and p.burst_restante > 0 and p not in fila and p != proc_atual:
                        fila.append(p)
                fila.append(proc_atual)
                proc_atual = None
                tempo_quantum = 0
                trocas_contexto += 1
        else:
            gantt.append((tempo, "IDLE"))

        tempo += 1

    return gantt, processos, trocas_contexto