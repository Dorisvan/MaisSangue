class Doacao():
    def __init__(self, data, local_destino, usuario_cpf, solicitacao_codigo):
        self.data = data
        self.local_destino = local_destino
        self.usuario_cpf = usuario_cpf
        self.solicitacao_codigo = solicitacao_codigo

    def getData(self):
        return self.data

    def setData(self, data):
        self.data = data

    def getLocal_destino(self):
        return self.local_destino

    def setLocal_destino(self, local_destino):
        self.local_destino = local_destino


    def setUsuario_cpf(self, usuario_cpf):
        self.usuario_cpf = usuario_cpf

    def getUsuario_cpf(self):
        return self.usuario_cpf
