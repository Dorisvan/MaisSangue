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


    def Listar(self, codigo):
        try:
            cursor = self.con.cursor()
            if codigo != None:
                sql = "SELECT DISTINCT d.codigo, d.data, d.local_destino, u.tipo_sanguineo, solicitacao_codigo FROM Doacao as d, Usuario as u WHERE d.usuario_codigo=%s"
                cursor.execute(sql, (codigo,))
                doacao = cursor.fetchall()
                return doacao
            else:
                sql = "SELECT DISTINCT d.codigo, d.data, d.local_destino, u.tipo_sanguineo, solicitacao_codigo  FROM Doacao as d, Usuario as u WHERE d.Usuario_codigo = u.codigo ORDER BY u.tipo_sanguineo"
                cursor.execute(sql,)
                doacoes = cursor.fetchall()
                return doacoes
        except:
            return None

    def Busca_avancada(self, termo, usuario_codigo, tipo):
        try:
            if tipo != None:
                sql = "SELECT * FROM Solicitacao WHERE codigo LIKE %s OR data LIKE %s OR urgencia LIKE %s OR local_internacao LIKE %s OR situacao LIKE %s"
                sql2 = "SELECT DISTINCT d.usuario_codigo, d.data, d.local_destino, u.tipo_sanguineo, d.Solicitacao_codigo FROM Doacao as d, Usuario as u WHERE d.Usuario_codigo = %s AND (d.codigo LIKE %s OR d.data LIKE %s OR d.local_destino LIKE %s OR d.Solicitacao_codigo LIKE %s OR d.Usuario_codigo LIKE %s OR u.tipo_sanguineo LIKE %s)"
                cursor = self.con.cursor()
                cursor.execute(sql2, (usuario_codigo, termo, termo, termo, termo, termo, termo))
                resultado = cursor.fetchall()
                return resultado

            else:
                sql = "SELECT * FROM Solicitacao WHERE codigo LIKE %s OR data LIKE %s OR urgencia LIKE %s OR local_internacao LIKE %s OR situacao LIKE %s"
                sql2 = "SELECT DISTINCT d.usuario_codigo, d.data, d.local_destino, u.tipo_sanguineo, d.Solicitacao_codigo FROM Doacao as d, Usuario as u WHERE d.codigo LIKE %s OR d.data LIKE %s OR d.local_destino LIKE %s OR d.Solicitacao_codigo LIKE %s OR d.Usuario_codigo LIKE %s OR u.tipo_sanguineo LIKE %s"
                cursor = self.con.cursor()
                cursor.execute(sql2, (termo, termo, termo, termo, termo, termo))
                resultado = cursor.fetchall()
                return resultado

        except:
            return("Não há nenhum usuário com esse dado informado no sistema.")


    def Checar_ultimadoacao(self, codigo):
        try:
            if codigo != None:

                sql = "SELECT u.codigo FROM Usuario as u, Doacao as d WHERE %s NOT IN(SELECT d.Usuario_codigo FROM Doacao as d) GROUP BY u.codigo"
                cursor = self.con.cursor()
                cursor.execute(sql, (codigo,))
                resultado1 = cursor.fetchall()

                if resultado1 != None:
                    resultado_final = 1
                else:
                    sql1 = 'SELECT * FROM Doacao WHERE codigo = %s AND CURDATE() > DATE_ADD((SELECT MAX(data) FROM Doacao WHERE codigo = %s GROUP BY codigo), INTERVAL 120 DAY);'
                    cursor = self.con.cursor()
                    cursor.execute(sql1, (codigo, codigo))
                    resultado1 = cursor.fetchall()
                    if resultado1 != None:
                        resultado_final = 1
                    else:
                        resultado_final = None

                return resultado_final

            else:
                sql = 'SELECT u.codigo FROM Usuario as u, Doacao as d WHERE u.codigo = d.Usuario_codigo AND CURDATE()>DATE_ADD((SELECT MAX(d.data) ORDER BY MAX(d.data) DESC LIMIT 1), INTERVAL 120 DAY)'
                cursor = self.con.cursor()
                cursor.execute(sql, )
                resultado = cursor.fetchall()
                return resultado
        except:
            None
