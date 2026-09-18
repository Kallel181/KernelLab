class Processo:
    def __init__(self, id, funcao, chegada, burst, prioridade, memoria, dispositivos):
        self.id = id
        self.funcao = funcao
        self.chegada = chegada
        self.burst_original = burst
        self.burst_restante = burst
        self.prioridade = prioridade
        self.memoria = memoria
        self.dispositivos = dispositivos
        
        self.tempo_inicio = None
        self.tempo_fim = None
        self.tempo_espera = 0
        self.tempo_retorno = 0
        self.tempo_resposta = None

    def reset(self):
        """Reseta o estado para reutilizar o processo em outro algoritmo."""
        self.burst_restante = self.burst_original
        self.tempo_inicio = None
        self.tempo_fim = None
        self.tempo_espera = 0
        self.tempo_retorno = 0
        self.tempo_resposta = None

def calcular_metricas_globais(processos, trocas_contexto):
    """Calcula as médias globais para um algoritmo."""
    n = len(processos)
    media_espera = sum(p.tempo_espera for p in processos) / n
    media_retorno = sum(p.tempo_retorno for p in processos) / n
    media_resposta = sum(p.tempo_resposta for p in processos) / n
    
    return {
        "media_espera": media_espera,
        "media_retorno": media_retorno,
        "media_resposta": media_resposta,
        "trocas_contexto": trocas_contexto
    }