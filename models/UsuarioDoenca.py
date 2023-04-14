class UsuarioDoenca():
    def __init__(self, usuario_cpf, doenca_id):
        self.usuario_cpf = usuario_cpf
        self.doenca_id = doenca_id

    def getUsuario_cpf(self):
        return self.usuario_cpf

    def setUsuario_cpf(self, usuario_cpf):
        self.usuario_cpf = usuario_cpf

    def getDoenca_id(self):
        return self.doenca_id

    def setDoenca_id(self, doenca_id):
        self.doenca_id = doenca_id