# KernelLab — Simulador de Gerenciamento de Recursos do SO

O KernelLab é um simulador modular de sistemas operacionais desenvolvido em Python. Ele foi projetado para reproduzir as decisões tomadas por um Kernel na gestão de CPU, memória virtual e acesso a dispositivos de E/S, permitindo avaliar e comparar o impacto de diferentes políticas em cenários de alta concorrência e criticidade.

---

## 1. Problema e Objetivo

### O Problema (Cenário MedControl Systems)
A plataforma da MedControl Systems gerencia equipamentos médicos conectados executando simultaneamente tarefas de monitoramento cardíaco, alarmes críticos, telemetria, geração de relatórios, backups e atualizações. Recentemente, foram identificados gargalos operacionais graves:
- Atrasos no processamento de alarmes críticos e aumento do tempo de resposta geral.
- Disputa acirrada por tempo de CPU e elevado número de trocas de contexto.
- Alta ocorrência de faltas de página (page faults).
- Risco de starvation de processos de baixa prioridade e concorrência no acesso a dispositivos de E/S (Rede, Disco e Áudio).

### O Objetivo
O KernelLab reproduz esse cenário e fornece um ambiente de testes para comparar quantitativamente diferentes algoritmos de escalonamento de CPU, substituição de páginas de memória e matrizes de controle de acesso de dispositivos, auxiliando na escolha da melhor arquitetura para o sistema.

---

## 2. Arquitetura do Simulador

O simulador é estruturado em pipeline discreto de tempo (tempo = 0, 1, 2, ...), simulando eventos a cada ciclo de relógio sem a necessidade de threads reais do SO hospedeiro.

- data/processes.json: Configuração e carga de trabalho dos processos
- src/main.py: Ponto de entrada e orquestrador do fluxo
- src/metrics.py: Estruturas de dados (Processo) e cálculo de métricas
- src/schedulers.py: Algoritmos de escalonamento da CPU
- src/memory.py: Algoritmos de gerenciamento de memória virtual
- src/devices.py: Matriz de controle de acesso (DAC) e sincronização de E/S
- src/visualization.py: Gerador de relatórios no terminal e gráficos Matplotlib
- tests/: Testes unitários do sistema
- requirements.txt: Dependências do projeto
- README.md: Documentação técnica

---

## 3. Algoritmos Implementados

- Escalonamento de CPU (Etapa 1):
  - FCFS (First-Come, First-Served): Atendimento por ordem de chegada (Não-preemptivo).
  - SJF (Shortest Job First): Prioriza processos com menor tempo de execução restante (Não-preemptivo).
  - Round Robin (RR): Alternância circular de tempo baseada em fatia (Quantum fixo).
  - Escalonamento por Prioridade: Execução baseada em nível de prioridade (Menor valor = Maior prioridade).
- Gerenciamento de Memória Virtual (Etapa 3):
  - FIFO (First-In, First-Out): Substitui a página residente há mais tempo na memória.
  - LRU (Least Recently Used): Substitui a página que permaneceu sem uso pelo maior período.
  - Optimal (Algoritmo Ótimo): Substitui a página que demorará mais tempo para ser consultada no futuro (Benchmark teórico).
- Controle de Dispositivos (Etapa 4):
  - Matriz de Controle de Acesso Discrecionária (DAC) mapeando permissões (Read, Write, Execute, Uso, Exclusivo).
  - Fila de requisições por dispositivo com controle de concorrência por mutex/semáforo simbólico.

---

## 4. Instruções de Instalação e Execução

### Pré-requisitos
- Python 3.10 ou superior.

### Passo a Passo

1. Clonar ou extrair o repositório:
   git clone https://github.com/Kallel181/KernelLab.git
   cd kernellab

2. Criar e ativar um ambiente virtual (recomendado):
   python -m venv venv
   source venv/bin/activate  # No Linux/macOS
   venv\Scripts\activate     # No Windows

3. Instalar as dependências:
   pip install -r requirements.txt

4. Executar o simulador:
   python src/main.py

---

## 5. Formato dos Dados de Entrada

Os processos são definidos em data/processes.json. Todos os atributos são totalmente parametrizáveis:

[
  {
    "id": "P1",
    "funcao": "Monitoramento cardíaco",
    "chegada": 0,
    "burst": 8,
    "prioridade": 1,
    "memoria": 120,
    "dispositivos": ["Rede"]
  },
  {
    "id": "P4",
    "funcao": "Emissão de alarme crítico",
    "chegada": 3,
    "burst": 2,
    "prioridade": 0,
    "memoria": 60,
    "dispositivos": ["Audio", "Rede"]
  }
]

---

## 6. Exemplos de Uso

### Alterando os Parâmetros da Simulação

- Mudar Carga dos Processos: Edite data/processes.json para adicionar novos processos ou alterar tempos de burst, chegada e prioridade.
- Ajustar Quantum do Round Robin: No arquivo src/main.py, altere o argumento quantum na chamada da função round_robin(processos_base, quantum=5).
- Alterar Sequência de Memória: Modifique a lista ref_paginas e o número de frames em src/main.py.

---

## 7. Instruções para Execução dos Testes

Para executar a suíte de testes funcionais das métricas e estruturas de dados:

python -m unittest discover -s tests

---

## 8. Resultados Principais

### Comparativo do Escalonamento de CPU

| Algoritmo | Tempo de Espera Médio | Tempo de Resposta Médio | Trocas de Contexto | Risco de Starvation | Atendimento do Alarme (P4) |
| --- | --- | --- | --- | --- | --- |
| FCFS | Alto | Alto | Baixo | Nulo | Ruim (Aguarda fila) |
| SJF | Menor Espera | Moderado | Baixo | Alto | Regular |
| Round Robin (Q=3) | Moderado | Baixo | Alto | Nulo | Moderado |
| Prioridade | Varia | Baixo p/ críticas | Baixo | Alto | Excelente |

### Gerenciamento de Memória (4 Frames, 17 Referências)

- FIFO: Apresenta maior taxa de page faults devido à insensibilidade à frequência/recência das requisições.
- LRU: Reduz significativamente o número de page faults ao explorar a localidade temporal.
- Optimal: Obtém a menor taxa de faltas teórica, servindo de piso comparativo.

---

## 9. Limitações e Possíveis Melhorias

### Limitações Atuais
- Modelagem de CPU Única: Não simula arquiteturas multicore ou multiprocessadas.
- I/O Não-Bloqueante Sintético: Os dispositivos de E/S são simulados isoladamente e não interrompem a CPU preemptivamente durante a simulação de burst.

### Possíveis Melhorias Futuras
1. Implementação de Múltiplas Filas com Realimentação (MLFQ).
2. Mecanismo de Aging (Envelhecimento) para evitar starvation.
3. Interface Gráfica Web interativa com Streamlit.