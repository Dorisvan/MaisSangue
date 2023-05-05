class UsuarioDAO():
    def __init__(self, con):
        self.con = con

    # CRUD --> Create, Retrieve, Uptade, Delete <--
    def Inserir(self, usuario):
        try:
            sql = "INSERT INTO Usuario(cpf, nome, idade, peso, tipo_sanguineo, cep, cidade, email, senha, telefone, opcao_doacao, estado_sessao) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

            cursor = self.con.cursor()
            cursor.execute(sql, (usuario.cpf, usuario.nome, usuario.idade, usuario.peso, usuario.tipo_sanguineo, usuario.cep, usuario.cidade, usuario.email, usuario.senha, usuario.telefone, usuario.opcao_doacao, usuario.estado_sessao))

            self.con.commit()

            codigo = cursor.lastrowid

            return codigo

        except:
            return 0


    def Listar(self, cpf=None):
        try:
            cursor = self.con.cursor()
            if cpf != None:
                # pegar somente uma planta
                sql = "SELECT * FROM Usuario WHERE cpf=%s"
                cursor.execute(sql, (cpf,))
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

    def Atualizar(self, usuario):
        try:
            sql = "UPDATE Usuario " \
                  "SET cpf=%s, nome=%s, " \
                  "idade=%s, peso=%s, tipo_sanguineo=%s, cep=%s, cidade=%s, email=%s, senha=%s, telefone=%s" \
                  "WHERE cpf=%s"

            cursor = self.con.cursor()
            cursor.execute(sql, (usuario.cpf, usuario.nome, usuario.idade, usuario.peso, usuario.tipo_sanguineo, usuario.cep, usuario.cidade, usuario.email, usuario.senha, usuario.telefone, usuario.cpf))
            self.con.commit()
            return cursor.rowcount

        except:
            return 0


    def Excluir(self, cpf):
        try:
            sql = "DELETE FROM Usuario WHERE cpf = %s"
            cursor = self.con.cursor()
            cursor.execute(sql, (cpf,))
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