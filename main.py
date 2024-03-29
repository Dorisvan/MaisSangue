# Bibliotecas e classes

from flask import Flask, render_template, g, request, redirect, url_for, session, flash

import mysql.connector

from models.Doacao import Doacao
from models.DoacaoDAO import DoacaoDAO
from models.Solicitacao import Solicitacao
from models.SolicitacaoDAO import SolicitacaoDAO
from models.Usuario import Usuario
from models.UsuarioDAO import UsuarioDAO
from models.Doenca import Doenca
from models.DoencaDAO import DoencaDAO
from models.UsuarioDoenca import UsuarioDoenca
from models.UsuarioDoencaDAO import UsuarioDoencaDAO


# Variáveis gerais

app = Flask(__name__)
app.secret_key = "senha123"


DB_HOST = "localhost"
DB_USER = "root"
DB_PASS = ""
DB_NAME = "doacaodb"

# Autorizações

app.auth = {
    # acao: { perfil:permissao }
    'painel': {0:1, 1:1},
    'logout': {0:1, 1:1},
    'perfil': {0:1, 1:1},
    'solicitar': {0:1, 1:1},
    'doar': {0:1, 1:1},
    'listar_usuario': {0:1, 1:1},
    'solicitacoes': {0:1, 1:1},
    'doacoes': {0:1, 1:1},
    'historico_doencas': {0:1, 1:1}
}


@app.before_request
def autorizacao():
    acao = request.path[1:]
    acao = acao.split('/')
    if len(acao)>=1:
        acao = acao[0]

    acoes = app.auth.keys()
    if acao in list(acoes):
        if session.get('logado') is None:
            return redirect(url_for('login'))
        else:
            estado_sessao = session['logado']['estado_sessao']
            if app.auth[acao][estado_sessao]==0:
                return redirect(url_for('painel'))


# Conexão com o banco de dados

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME
        )
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


# Páginas simples

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/como_doar')
def como_doar():
    return render_template("como_doar.html", titulo="Como doar")


@app.route('/perguntas_frequentes')
def perguntas_frequentes():
    return render_template("#perguntas_frequentes", titulo="Painel")


@app.route('/painel')
def painel():
    return render_template("painel.html", titulo="Painel")


# Funções de Cadastro/Login/Logout

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        cpf = request.form['cpf']
        cep = request.form['cep']
        cidade = request.form['cidade']
        idade = request.form['dt_nasc']
        tipo_sanguineo = request.form['tipo_sanguineo']
        peso = request.form['peso']
        telefone = request.form['telefone']
        opcao_doacao = request.form['opcao_doacao']
        senha = request.form['senha']

        usuario = Usuario(cpf, nome, idade, peso, tipo_sanguineo, cep, cidade, email, senha, 0, telefone, opcao_doacao)
        dao = UsuarioDAO(get_db())
        codigo = dao.Inserir(usuario)
        print(codigo)

        if codigo >= 0:
            flash("Usuário cadastrado com sucesso!", "success")
        else:
            flash("Erro ao cadastrar!", "danger")

    vartitulo = "Cadastro"
    return render_template("cadastro.html", titulo=vartitulo)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        # Verificar dados
        dao = UsuarioDAO(get_db())
        usuario = dao.autenticar(email, senha)

        if usuario is not None:
            session['logado'] = {
                'cpf': usuario[0],
                'nome': usuario[1],
                'email': usuario[7],
                'estado_sessao': usuario[13]
            }
            return redirect(url_for('painel'))
        else:
            flash("Erro ao efetuar login! Verifique seus dados novamente.", "danger")

    return render_template("login.html", titulo="Login")


@app.route('/logout')
def logout():
    session['logado'] = None
    session.clear()
    return redirect(url_for('index'))


# Funções de CREATE

@app.route('/solicitar',  methods=['GET', 'POST'])
def solicitar():
    daoUsuario = UsuarioDAO(get_db())

    if request.method == 'POST':
        data = request.form['data']
        urgencia = request.form['urgencia']
        local_internacao = request.form['local_internacao']
        usuario_cpf = request.form['usuario_cpf']
        situacao = "Pendente"

        solicitacao = Solicitacao(data, urgencia, local_internacao, situacao, usuario_cpf)

        dao = SolicitacaoDAO(get_db())
        codigo = dao.Inserir(solicitacao)

        if codigo > 0:
            flash("Solicitação cadastrada com sucesso! Código %d" % codigo, "success")
        else:
            flash("Erro ao cadastrar solicitação! Verifique seus dados novamente.", "danger")

    usuarios_db = daoUsuario.Listar()
    return render_template("solicitar.html", titulo="Solicitação", usuarios=usuarios_db,)


@app.route('/doar',  methods=['GET', 'POST'])
def doar():
    if request.method == 'POST':
        data = request.form['data']
        local_destino = request.form['local_destino']
        usuario_cpf= request.form['usuario_cpf']
        solicitacao_codigo = request.form['solicitacao_codigo']

        doacao = Doacao(data, local_destino, usuario_cpf, solicitacao_codigo)
        dao = DoacaoDAO(get_db())
        codigo = dao.Inserir(doacao)

        if codigo > 0:
            flash("Doação cadastrada com sucesso! Código %d" % codigo, "success")
        else:
            flash("Erro ao cadastrar doação! Verifique as informações novamente.", "danger")

    return render_template("doar.html", titulo="Doação")


@app.route('/historico_doencas',  methods=['GET', 'POST'])
def historico_doencas():
    if request.method == 'POST':
        usuario_cpf = request.form['usuario_cpf']
        doenca_id = request.form['doenca_id']

        usuariodoenca = UsuarioDoenca(usuario_cpf, doenca_id)

        dao = UsuarioDoencaDAO(get_db())
        codigo = dao.Inserir(usuariodoenca)

        if codigo > 0:
            flash("Estado de saúde cadastrado com sucesso! Código %d" % codigo, "success")
        else:
            flash("Erro ao cadastrar estado de saúde!", "danger")

    return render_template("historico_doencas.html", titulo="Histórico de saúde")


# Funções de READ

@app.route('/listar_usuario', methods=['GET',])
def listar_usuario():
    dao = UsuarioDAO(get_db())
    usuarios_db = dao.Listar()
    return render_template("listar_usuario.html", usuarios=usuarios_db)


@app.route('/solicitacoes', methods=['GET',])
def listar_solicitacoes():
    dao = SolicitacaoDAO(get_db())
    solicitacoes_db = dao.Listar_Solicitacoes()
    return render_template("solicitacoes.html", solicitacoes=solicitacoes_db)


@app.route('/doacoes', methods=['GET',])
def doacoes():
    dao = DoacaoDAO(get_db())
    doacoes_db = dao.Listar()
    return render_template("doacoes.html", doacoes=doacoes_db)


@app.route('/listar_doacoes_por_data', methods=['GET',])
def listar_doacoes_por_data():
    dao = DoacaoDAO(get_db())
    doacoes_db = dao.Listar_por_data()
    return render_template("doacao_por_data.html", doacao=doacoes_db)


@app.route('/listar_historico', methods=['GET',])
def listar_doencas():
    dao = UsuarioDoencaDAO(get_db())
    usuariosdoencas_db = dao.Listar()
    return render_template("historico_doencas.html", usuariodoenca= usuariosdoencas_db)


# Funções de UPDATE

@app.route('/atualizar_usuario/<cpf>', methods=['GET', 'POST'])
def atualizar_usuario(cpf):
    dao = UsuarioDAO(get_db())

    if request.method == "POST":
        nome = request.form['nome']
        email = request.form['email']
        cpf = request.form['cpf']
        cep = request.form['cep']
        cidade = request.form['cidade']
        idade = request.form['dt_nasc']
        tipo_sanguineo = request.form['tipo_sanguineo']
        peso = request.form['peso']
        telefone = request.form['telefone']
        situacao_doacao = request.form['situacao_doacao']
        senha = request.form['senha']

        usuario = Usuario(cpf, nome, idade, peso, tipo_sanguineo, cep, cidade, email, senha, telefone, situacao_doacao)
        usuario.setCpf(cpf)
        ret = dao.Atualizar(usuario)

        if ret > 0:
            flash("Atualização concluída com sucesso! Código %d" % ret, "success")
        else:
            flash("Erro ao atualizar!", "danger")


    usuario_db = dao.Listar(cpf)
    return render_template("perfil_usuario.html", usuario = usuario_db)


@app.route('/atualizar_solicitacao/<codigo>', methods=['GET', 'POST'])
def atualizar_solicitacao(codigo):
    dao = SolicitacaoDAO(get_db())

    if request.method == "POST":
        data = request.form['data']
        urgencia = request.form['urgencia']
        local_internacao = request.form['local_internacao']
        usuario_cpf = request.form['usuario_cpf']
        situacao = request.form['situacao']

        solicitacao = Solicitacao(data, urgencia, local_internacao, situacao, usuario_cpf)
        solicitacao.setId(codigo)

        ret = dao.Atualizar(solicitacao)

        if ret > 0:
            flash("Atualização concluída com sucesso! Código %d" % ret, "success")
        else:
            flash("Erro ao atualizar!", "danger")

    solicitacao_db = dao.Listar(codigo)
    return render_template("atualizar_solicitacao.html", solicitacao=solicitacao_db)


@app.route('/doar_solicitacao/<int:codigo>', methods=['GET', 'POST'])
def doar_solicitacao(codigo):
    dao = SolicitacaoDAO(get_db())
    dao2 = DoacaoDAO(get_db())

    if request.method == "POST":
        data = request.form['data']
        urgencia = request.form['urgencia']
        usuario_cpf = request.form['usuario_cpf']
        local_internacao = request.form['local_internacao']


        doacao = Doacao(data, urgencia, local_internacao, usuario_cpf)
        ret = dao2.Inserir(doacao)

        if codigo > 0:
            flash("Atualizar com sucesso! Código %d" % codigo, "success")
        else:
            flash("Erro ao atualizar!", "danger")

    solicitacao_db = dao.Listar(codigo)
    return render_template("doar_solicitacao.html", solicitacao= solicitacao_db)


# Funções de DELETE

@app.route('/excluir_solicitacao/<codigo>', methods=['GET',])
def excluir_solicitacao(codigo):
    dao = Solicitacao(get_db())
    ret = dao.Excluir(codigo)
    if ret == 1:
        flash(f"Solicitação {codigo} excluída com sucesso!", "success")
    else:
        flash(f"Erro ao excluir solicitação {codigo}.", "danger")
    return redirect(url_for('solicitacoes.html'))


@app.route('/excluir_doenca/<codigo>', methods=['GET',])
def excluir_doenca(codigo):
    dao = UsuarioDoenca(get_db())
    ret = dao.Excluir(codigo)
    if ret == 1:
        flash(f"Estado de saúde {codigo} excluído com sucesso!", "success")
    else:
        flash(f"Erro ao excluir estado de saúde{codigo}.", "danger")
    return redirect(url_for('perfil_usuario.html'))


# HOST


if __name__=='__main__':
    app.run(host="0.0.0.0", port=80, debug=True)
