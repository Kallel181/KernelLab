def fifo(sequencia, num_frames=4):
    frames = []
    page_faults = 0
    page_hits = 0
    historico = []

    for pag in sequencia:
        if pag in frames:
            page_hits += 1
        else:
            page_faults += 1
            if len(frames) >= num_frames:
                frames.pop(0)  # Remove o mais antigo
            frames.append(pag)
        historico.append(list(frames))

    taxa = (page_faults / len(sequencia)) * 100
    return page_faults, page_hits, taxa, historico

def lru(sequencia, num_frames=4):
    frames = []
    page_faults = 0
    page_hits = 0
    historico = []

    for pag in sequencia:
        if pag in frames:
            page_hits += 1
            frames.remove(pag)
            frames.append(pag)  # Move para o final (mais recente)
        else:
            page_faults += 1
            if len(frames) >= num_frames:
                frames.pop(0)  # Remove o menos recentemente usado
            frames.append(pag)
        historico.append(list(frames))

    taxa = (page_faults / len(sequencia)) * 100
    return page_faults, page_hits, taxa, historico

def optimal(sequencia, num_frames=4):
    frames = []
    page_faults = 0
    page_hits = 0
    historico = []

    for i, pag in enumerate(sequencia):
        if pag in frames:
            page_hits += 1
        else:
            page_faults += 1
            if len(frames) < num_frames:
                frames.append(pag)
            else:
                # Procura a página que vai demorar mais para ser usada no futuro
                futuro = sequencia[i+1:]
                pior_indice = -1
                pag_para_remover = None

                for f in frames:
                    if f not in futuro:
                        pag_para_remover = f
                        break
                    else:
                        idx = futuro.index(f)
                        if idx > pior_indice:
                            pior_indice = idx
                            pag_para_remover = f

                frames.remove(pag_para_remover)
                frames.append(pag)

        historico.append(list(frames))

    taxa = (page_faults / len(sequencia)) * 100
    return page_faults, page_hits, taxa, historico