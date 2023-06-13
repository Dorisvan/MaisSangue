class DoacaoDAO():
    def __init__(self, con):
        self.con = con

    # CRUD --> Create, Retrieve, Uptade, Delete <--
    def Inserir(self, Doacao, usuario_tipo_sanguineo, solicitante_tipo_sanguineo):
        try:
            cursor = self.con.cursor()
            situacao = "Pendente"
            sql1 = "SELECT u.codigo FROM Usuario as u, UsuarioDoenca as ud, Doacao as d, Solicitacao as s WHERE u.codigo = %s AND u.tipo_sanguineo = %s AND u.codigo NOT IN ud.codigo_usuario AND (SELECT Solicitacao WHERE s.codigo = %s AND s.situacao = %s)"
            cursor.execute(sql1, (Doacao.usuario_codigo, solicitante_tipo_sanguineo, Doacao.solicitacao_codigo, situacao,))
            usuario = cursor.fetchone()
            print(usuario)
            return usuario

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

