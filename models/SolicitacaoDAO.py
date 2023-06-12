class SolicitacaoDAO():
    def __init__(self, con):
        self.con = con

    # CRUD --> Create, Retrieve, Uptade, Delete <--

    def Listar_Solicitacoes(self):
        cursor = self.con.cursor()
        try:
            sql = "SELECT s.codigo, s.data, s.urgencia, s.local_internacao, u.tipo_sanguineo, s.situacao FROM Solicitacao as s, Usuario as u WHERE s.Usuario_codigo = u.codigo GROUP BY s.codigo, u.tipo_sanguineo, s.situacao"
            cursor.execute(sql, )
            solicitacoes = cursor.fetchall()
            return solicitacoes
        except:
            return None

    def Inserir(self, Solicitacao):
        try:
            sql = "INSERT INTO Solicitacao(data, urgencia, local_internacao, situacao, usuario_codigo) VALUES (%s, %s, %s, %s, %s)"

            cursor = self.con.cursor()
            cursor.execute(sql, (Solicitacao.data, Solicitacao.urgencia, Solicitacao.local_internacao, Solicitacao.situacao, Solicitacao.usuario_codigo))

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
                sql = "SELECT * FROM Solicitacao WHERE codigo=%s"
                cursor.execute(sql, (codigo,))
                solicitacao = cursor.fetchone()
                return solicitacao
            else:
                # pegar todas as plantas
                sql = "SELECT * FROM Solicitacao"
                cursor.execute(sql)
                solicitacao = cursor.fetchall()
                return solicitacao
        except:
            return None

    def Atualizar(self, Solicitacao):
        try:
            sql = "UPDATE Solicitacao " \
                  "SET data=%s, urgencia=%s, " \
                  "local_internacao=%s, situacao=%s, usuario_codigo=%s" \
                  "WHERE codigo=%s"

            cursor = self.con.cursor()
            cursor.execute(sql, (Solicitacao.data, Solicitacao.urgencia, Solicitacao.local_internacao, Solicitacao.situacao, Solicitacao.usuario_codigo, Solicitacao.id))
            self.con.commit()
            return cursor.rowcount
        except:
            return 0


    def Pendentes(self):

        Certo = "Ok"
        Pendente = "Pendente"
        Situacao = "Situacao"

        try:
            sql = "SELECT d.codigo, d.cpf, d.nome, d.idade, d.peso, d.tipo_sanguineo, d.estado, d.cidade, d.telefone, d.email, MAX(doa.data) as ultima_doacao, CASE  WHEN d.codigo = doa.Doador_codigo AND CURDATE()>DATE_ADD((SELECT MAX(doa.data) ORDER BY MAX(doa.data) DESC LIMIT 1), INTERVAL 120 DAY) AND d.peso > 50 THEN  %s END as %s FROM Doacao as doa, Doador as d, historicodoador as hd WHERE doa.data = (SELECT MAX(doa.data) ORDER BY MAX(doa.data) DESC LIMIT 1 ) AND d.codigo = doa.Doador_codigo GROUP BY d.codigo; "

            cursor = self.con.cursor()
            cursor.execute(sql, (Certo, Situacao))
            resultado = cursor.fetchall()

            return resultado

        except:
            return("Não há animais pendentes.")


    def Excluir(self, codigo):
        try:
            sql = "DELETE FROM Solicitacao WHERE codigo = %s"
            cursor = self.con.cursor()
            cursor.execute(sql, (codigo,))
            self.con.commit()
            return cursor.rowcount
        except:
            return 0

    def Busca_avancada(self, termo):
        try:
            sql = "SELECT * FROM Solicitacao WHERE codigo LIKE %s OR data LIKE %s OR urgencia LIKE %s OR local_internacao LIKE %s OR situacao LIKE %s"
            sql2 = "SELECT DISTINCT s.codigo, s.data, s.urgencia, s.local_internacao, u.tipo_sanguineo, s.situacao FROM Solicitacao as s, Usuario as u WHERE s.Usuario_codigo = u.codigo AND s.codigo LIKE %s OR s.data LIKE %s OR s.urgencia LIKE %s OR s.local_internacao LIKE %s OR u.tipo_sanguineo LIKE %s OR s.situacao LIKE %s"
            cursor = self.con.cursor()
            cursor.execute(sql2, (termo, termo, termo, termo, termo, termo,))
            resultado = cursor.fetchall()

            return resultado
        except:
            return("Não há nenhuma solicitação com esse dado informado no sistema.")
