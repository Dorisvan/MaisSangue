class UsuarioDoenca():
    def __init__(self, doenca_id, usuario_codigo):
        self.usuario_codigo = usuario_codigo
        self.doenca_id = doenca_id

    def getUsuario_codigo(self):
        return self.usuario_codigo

    def setUsuario_codigo(self, usuario_codigo):
        self.usuario_codigo = usuario_codigo

    def getDoenca_id(self):
        return self.doenca_id

    def setDoenca_id(self, doenca_id):
        self.doenca_id = doenca_id