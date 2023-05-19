class Usuario():
    def __init__(self, cpf, nome, dt_nasc, peso, tipo_sanguineo, cep, cidade, email, senha, telefone="", opcao_doacao="", estado_doacao="",  nivel_usuario="", estado_sessao=""):
        self.id = 0
        self.cpf = cpf
        self.nome = nome
        self.dt_nasc = dt_nasc
        self.peso = peso
        self.tipo_sanguineo = tipo_sanguineo
        self.cep = cep
        self.cidade = cidade
        self.email = email
        self.senha = senha
        self.telefone = telefone
        self.opcao_doacao = opcao_doacao
        self.estado_doacao = estado_doacao
        self.nivel_usuario = nivel_usuario
        self.estado_sessao = estado_sessao


    def setId(self, id):
        self.id = id

    def getId(self):
        self.id


    def getCpf(self):
        return self.cpf

    def setCpf(self, cpf):
        self.cpf = cpf


    def getNome(self):
        return self.nome

    def setNome(self, nome):
        self.nome = nome


    def getDt_nasc(self):
        return self.dt_nasc

    def setDt_nasc(self, dt_nasc):
        self.dt_nasc = dt_nasc


    def getPeso(self):
        return  self.peso

    def setPeso(self, peso):
        self.peso = peso


    def getTipo_sanguineo(self):
        return self.tipo_sanguineo

    def setTipo_sanguineo(self, tipo_sanguineo):
        self.tipo_sanguineo = tipo_sanguineo


    def getEstado(self):
        return self.estado_sessao

    def setEstado(self, estado):
        self.estado_sessao = estado


    def getCidade(self):
        return self.cidade

    def setCidade(self, cidade):
        self.cidade = cidade


    def getTelefone(self):
        return self.telefone

    def setTelefone(self, telefone):
        self.telefone = telefone


    def getEmail(self):
        return self.email

    def setEmail(self, email):
        self.email = email





