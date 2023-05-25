class UsuarioDAO():
    def __init__(self, con):
        self.con = con

    # CRUD --> Create, Retrieve, Uptade, Delete <--
    def Inserir(self, usuario):
        try:
            sql = "INSERT INTO Usuario(cpf, nome, dt_nasc, peso, tipo_sanguineo, cep, cidade, email, senha, telefone, opcao_doacao, estado_sessao) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

            cursor = self.con.cursor()
            cursor.execute(sql, (usuario.cpf, usuario.nome, usuario.dt_nasc, usuario.peso, usuario.tipo_sanguineo, usuario.cep, usuario.cidade, usuario.email, usuario.senha, usuario.telefone, usuario.opcao_doacao, usuario.estado_sessao))

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
                sql = "SELECT * FROM Usuario WHERE codigo=%s"
                cursor.execute(sql, (codigo,))
                usuario = cursor.fetchone()
                return usuario
            else:
                # pegar todas as plantas
                sql = "SELECT * FROM Usuario"
                cursor.execute(sql)
                usuarios = cursor.fetchall()
                return usuarios
        except:
            return None


    def Buscar_email(self, email):
        sql = "SELECT * FROM Usuario WHERE email=%s"

        cursor = self.con.cursor()
        cursor.execute(sql, (email,))

        return cursor.fetchone()

    def Atualizar(self, usuario):
        try:
            sql = "UPDATE Usuario " \
                  "SET cpf=%s, nome=%s, " \
                  "idade=%s, peso=%s, tipo_sanguineo=%s, cep=%s, cidade=%s, email=%s, senha=%s, telefone=%s" \
                  "WHERE codigo=%s"

            cursor = self.con.cursor()
            cursor.execute(sql, (usuario.cpf, usuario.nome, usuario.idade, usuario.peso, usuario.tipo_sanguineo, usuario.cep, usuario.cidade, usuario.email, usuario.senha, usuario.telefone, usuario.codigo))
            self.con.commit()
            return cursor.rowcount

        except:
            return 0


    def Excluir(self, codigo):
        try:
            sql = "DELETE FROM Usuario WHERE codigo = %s"
            cursor = self.con.cursor()
            cursor.execute(sql, (codigo,))
            self.con.commit()
            return cursor.rowcount
        except:
            return 0


    def autenticar(self, email, senha):
        try:
            sql = "SELECT * FROM Usuario WHERE email=%s AND senha=%s"

            cursor = self.con.cursor()
            cursor.execute(sql, (email, senha))

            usuario = cursor.fetchone()  # lastrowid, fetchone, fetchall
            return usuario

        except:
            return None