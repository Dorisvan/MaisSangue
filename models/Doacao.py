class Doacao():
    def __init__(self, data, local_destino, solicitacao_codigo, usuario_codigo):
        self.data = data
        self.local_destino = local_destino
        self.usuario_codigo = usuario_codigo
        self.solicitacao_codigo = solicitacao_codigo

    def getData(self):
        return self.data

    def setData(self, data):
        self.data = data

    def getLocal_destino(self):
        return self.local_destino

    def setLocal_destino(self, local_destino):
        self.local_destino = local_destino


    def setUsuario_codigo(self, usuario_codigo):
        self.usuario_codigo = usuario_codigo

    def getUsuario_codigo(self):
        return self.usuario_codigo
