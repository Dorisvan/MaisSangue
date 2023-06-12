class Solicitacao():
    def __init__(self, data, urgencia, local_internacao, situacao, usuario_codigo):
        self.id = 0
        self.data = data
        self.urgencia = urgencia
        self.local_internacao = local_internacao
        self.situacao = situacao
        self.usuario_codigo = usuario_codigo


    def setId(self, id):
        self.id = id

    def getId(self):
        return self.id


    def getData(self):
        return self.data

    def setData(self, data):
        self.data = data


    def getUrgencia(self):
        return self.urgencia

    def setUrgencia(self, urgencia):
        self.urgencia = urgencia


    def getTipo_sanguineo(self):
        return self.tipo_sanguineo

    def setTipo_sanguineo(self, tipo_sanguineo):
        self.tipo_sanguineo = tipo_sanguineo


    def getLocal_internacao(self):
        return self.local_internacao

    def setLocal_internacao(self, local_internacao):
        self.local_internacao = local_internacao

