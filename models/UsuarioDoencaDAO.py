class UsuarioDoencaDAO():
    def __init__(self, con):
        self.con = con

    # CRUD --> Create, Retrieve, Uptade, Delete <--
    def Inserir(self, usuariodoenca):
        try:
            sql = "INSERT INTO UsuarioDoenca(Doenca_id, Usuario_codigo) VALUES (%s, %s)"

            cursor = self.con.cursor()
            cursor.execute(sql, (usuariodoenca.doenca_id, usuariodoenca.usuario_codigo,))

            self.con.commit()

            codigo = cursor.lastrowid
            return codigo

        except:
            return 0

    def Listar(self, codigo, tipo):
        try:
            cursor = self.con.cursor()
            if codigo != None:
                # pegar somente uma planta
                sql = "SELECT ud.Usuario_codigo, u.nome, d.id, d.nome FROM UsuarioDoenca as ud, Usuario as u, Doenca as d WHERE ud.Usuario_codigo = %s AND ud.Doenca_id = d.id"
                cursor.execute(sql, (codigo, ))
                usuariodoenca = cursor.fetchall()
                if tipo == "verificar" and usuariodoenca == []:
                    return None
                else:
                    return usuariodoenca
            else:
                # pegar todas as plantas
                sql = 'SELECT ud.Usuario_codigo, u.nome, d.id, d.nome FROM UsuarioDoenca as ud, Usuario as u, Doenca as d WHERE ud.Usuario_codigo = u.codigo AND ud.Doenca_id = d.id'
                cursor.execute(sql)
                usuario_doenca = cursor.fetchall()
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
