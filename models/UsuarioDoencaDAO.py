class UsuarioDoencaDAO():
    def __init__(self, con):
        self.con = con

    # CRUD --> Create, Retrieve, Uptade, Delete <--
    def Inserir(self, UsuarioDoenca):
        try:
            sql = "INSERT INTO UsuarioDoenca(Doenca_id, Usuario_cpf) VALUES (%s, %s)"

            cursor = self.con.cursor()
            cursor.execute(sql, (UsuarioDoenca.doenca_id, UsuarioDoenca.usuario_cpf))

            self.con.commit()

            codigo = cursor.lastrowid
            return codigo

        except:
            return 0

    def Listar(self, codigo=None):
        try:
            cursor = self.con.cursor()
            if codigo != None:
                # pegar somente uma planta
                sql = "SELECT * FROM UsuarioDoenca WHERE usuario_cpf=%s"
                cursor.execute(sql, (codigo,))
                usuariodoenca = cursor.fetchone()
                return usuariodoenca
            else:
                # pegar todas as plantas
                sql = "SELECT * FROM UsuarioDoenca"
                cursor.execute(sql)
                usuario_doenca= cursor.fetchall()
                return usuario_doenca
        except:
            return None

    def Deletar(self, UsuarioDoenca):
        try:
            sql = "DELETE FROM UsuarioDoenca WHERE usuario_cpf = %s"
            cursor = self.con.cursor()
            cursor.execute(sql, (UsuarioDoenca.usuario_cpf,))
            self.con.commit()
            return cursor.rowcount
        except:
            return 0
