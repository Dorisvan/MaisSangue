class DoacaoDAO():
    def __init__(self, con):
        self.con = con

    # CRUD --> Create, Retrieve, Uptade, Delete <--
    def Inserir(self, Doacao):
        try:
            sql = "INSERT INTO Doacao(data, local_destino, solicitacao_codigo, usuario_codigo) VALUES (%s, %s, %s, %s)"

            cursor = self.con.cursor()
            cursor.execute(sql, (Doacao.data, Doacao.local_destino, Doacao.solicitacao_codigo, Doacao.usuario_codigo))

            self.con.commit()

            codigo = cursor.lastrowid

            situacao = "Atendida"

            sql = "UPDATE Solicitacao SET situacao=%s WHERE codigo=%s"

            cursor = self.con.cursor()
            cursor.execute(sql, (situacao, Doacao.solicitacao_codigo,))
            self.con.commit()

            cursor = self.con.cursor()
            sql2 = 'SELECT u.email FROM Usuario as u, Solicitacao as s ' \
                   'WHERE u.codigo = s.Usuario_codigo AND s.codigo = %s'

            cursor.execute(sql2, (Doacao.solicitacao_codigo,))

            email = cursor.fetchone()

            return (codigo, email)


        except:
            return 0, 0

    def Listar_por_data(self, cpf=None):
        try:
            cursor = self.con.cursor()
            if cpf != None:
                sql = "SELECT * FROM Doacao WHERE Usuario_cpf = Doacao.usuario_cpf ORDER BY Doacao.data DESC;"
                cursor.execute(sql, (cpf,))
                doacao = cursor.fetchall()

                return doacao
            else:
                sql = "SELECT d.codigo, d.data, s.urgencia, d.local_destino, s.usuario_cpf * FROM Doacao as d, Usuario as u, Solicitacao as s WHERE u.cpf = d.usuario_cpf ORDER BY d.data DESC;"
                cursor.execute(sql, (cpf,))
                doacao = cursor.fetchall()

                return doacao
        except:
            return None


    '''def Checagem(self, Doacao, Solicitacao, Usuario):
        try:
            if Doacao.usuario_cpf == Usuario.cpf and Solicitacao[4]'''


    def Listar(self, codigo=None):
        try:
            cursor = self.con.cursor()
            if codigo != None:
                sql = "SELECT * FROM Doacao WHERE codigo=%s"
                cursor.execute(sql, (codigo,))
                doacao = cursor.fetchone()
                return doacao
            else:
                sql = "SELECT d.codigo, d.data, d.local_destino, u.tipo_sanguineo, solicitacao_codigo  FROM Doacao as d, Usuario as u WHERE d.Usuario_codigo = u.codigo ORDER BY u.tipo_sanguineo"
                cursor.execute(sql,)
                doacoes = cursor.fetchall()
                return doacoes
        except:
            return None

