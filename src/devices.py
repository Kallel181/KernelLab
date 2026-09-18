class MatrizAcesso:
    def __init__(self):
        # Matriz [Processo][Dispositivo] = Permissões
        self.permissoes = {
            "P1": {"Rede": ["R", "W", "X", "Uso", "Exclusivo"], "Disco": []},
            "P2": {"Rede": ["R", "W", "Uso"]},
            "P3": {"Disco": ["R", "W", "Uso"]},
            "P4": {"Audio": ["R", "W", "Uso", "Exclusivo"], "Rede": ["R", "W", "Uso"]},
            "P5": {"Disco": ["R", "W", "Uso"]},
            "P6": {"Disco": ["R", "W", "Uso"], "Rede": ["R", "W", "Uso"]}
        }

    def checar_permissao(self, processo_id, dispositivo, acao):
        perms = self.permissoes.get(processo_id, {}).get(dispositivo, [])
        return acao in perms

class Dispositivo:
    def __init__(self, nome):
        self.nome = nome
        self.em_uso_por = None
        self.fila_espera = []

    def solicitar_acesso(self, processo_id, matriz, exclusivo=False):
        if not matriz.checar_permissao(processo_id, self.nome, "Uso"):
            return f"ERRO: {processo_id} não possui autorização para usar {self.nome}."

        if self.em_uso_por is None:
            self.em_uso_por = processo_id
            return f"SUCESSO: {processo_id} adquiriu {self.nome}."
        else:
            self.fila_espera.append(processo_id)
            return f"BLOQUEADO: {processo_id} aguardando {self.nome} (ocupado por {self.em_uso_por})."

    def liberar_acesso(self, processo_id):
        if self.em_uso_por == processo_id:
            if self.fila_espera:
                self.em_uso_por = self.fila_espera.pop(0)
                return f"LIBERADO: {self.nome} repassado para {self.em_uso_por}."
            else:
                self.em_uso_por = None
                return f"LIBERADO: {self.nome} está livre."
        return f"ERRO: {processo_id} não detém o dispositivo {self.nome}."