# Bibliotecas e classes
import hashlib
import json
import smtplib

from flask import Flask, render_template, g, request, redirect, url_for, session, flash
from email.message import EmailMessage
from datetime import date
import datetime


import mysql.connector
import google.oauth2.credentials
import google_auth_oauthlib.flow
import requests
import os
import ssl

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

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


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
        dt_nasc = request.form['dt_nasc']
        tipo_sanguineo = request.form['tipo_sanguineo']
        peso = request.form['peso']
        telefone = request.form['telefone']
        opcao_doacao = request.form['opcao_doacao']
        senha = request.form['senha']

        usuario = Usuario(cpf, nome, dt_nasc, peso, tipo_sanguineo, cep, cidade, email, senha, 0, telefone, opcao_doacao)
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
                'codigo': usuario[0],
                'cpf': usuario[1],
                'nome': usuario[2],
                'tipo_sanguineo': usuario[5],
                'email': usuario[8],
                'nivel_usuario': usuario[13],
                'estado_sessao': usuario[14],
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


# Função de notificação


# Funções de CREATE

@app.route('/solicitar',  methods=['GET', 'POST'])
def solicitar():
    daoUsuario = UsuarioDAO(get_db())
    informacoes_usuario = session.get('logado')
    usuario_nivel = informacoes_usuario['nivel_usuario']
    usuario_codigo = informacoes_usuario['codigo']

    if request.method == 'POST':
        data = request.form['data']
        urgencia = request.form['urgencia']
        local_internacao = request.form['local_internacao']
        usuario_codigo = request.form['usuario_codigo']
        situacao = "Pendente"

        solicitacao = Solicitacao(data, urgencia, local_internacao, situacao, usuario_codigo)

        dao = SolicitacaoDAO(get_db())
        codigo = dao.Inserir(solicitacao)

        if codigo > 0:
            flash("Solicitação cadastrada com sucesso! Código %d" % codigo, "success")
        else:
            flash("Erro ao cadastrar solicitação! Verifique seus dados novamente.", "danger")

    usuarios_db = daoUsuario.Listar(usuario_codigo, "Checagem_individual")
    print(usuarios_db)
    return render_template("solicitar.html", titulo="Solicitação", usuarios=usuarios_db,)


@app.route('/doar',  methods=['GET', 'POST'])
def doar():
    if request.method == 'POST':
        data = request.form['data']
        local_destino = request.form['local_destino']
        usuario_codigo = request.form['usuario_codigo']
        solicitacao_codigo = request.form['solicitacao_codigo']

        dao = DoacaoDAO(get_db())
        dao1 = SolicitacaoDAO(get_db())
        dao2 = UsuarioDAO(get_db())
        dao3 = UsuarioDoencaDAO(get_db())

        # Obtenção/Verificação das informações compativéis

        solicitacao = dao1.Listar_Solicitacoes(solicitacao_codigo, "Verificacao")
        solicitacao = solicitacao[0]
        informacoes_solicitacao = list(solicitacao)
        informacoes_solicitacao[1] = str(informacoes_solicitacao[1])
        print(informacoes_solicitacao)

        usuario_doador = dao2.Listar(usuario_codigo, "Checagem_individual")
        informacoes_doador = list(usuario_doador)
        informacoes_doador[3] = str(informacoes_doador[3])
        print(informacoes_doador)

        historico_situacao = dao3.Listar(usuario_codigo, "verificar")
        print(historico_situacao)

        lista_data = dao.Checar_ultimadoacao(usuario_codigo)
        print(lista_data)

        if informacoes_doador[5] == informacoes_solicitacao[4] and informacoes_solicitacao[5] == "Pendente" and informacoes_doador[4] >= 60 and historico_situacao == None and lista_data != None:
            doacao = Doacao(data, local_destino, solicitacao_codigo, usuario_codigo)
            codigo, email = dao.Inserir(doacao)

            if codigo > 0:
                flash("Doação cadastrada com sucesso! Código %d" % codigo, "success")
                titulo = "Solicitação atendida."
                informe = "Caro usuário, sua solicitação acaba de ser atendida. Consulte a agência a qual você está vinculado."

                notificar(email, titulo, informe)
            else:
                flash("Erro ao cadastrar doação! Verifique as informações novamente.", "danger")
        else:
            flash("Você não cumpre com os requisitos básicos para doar.", "danger")

    return render_template("doar.html", titulo="Doação")



@app.route('/historico_doencas',  methods=['GET', 'POST'])
def historico_doencas():
    informacoes_usuario = session.get('logado')
    usuario_nivel = informacoes_usuario['nivel_usuario']
    usuario_codigo = informacoes_usuario['codigo']

    if usuario_nivel == 1:
        if request.method == 'POST':
            usuario_codigo = request.form['usuario_codigo']
            doenca_id = request.form['doenca_id']

            print(usuario_codigo)
            print(doenca_id)

            usuariodoenca = UsuarioDoenca(doenca_id, usuario_codigo)

            dao = UsuarioDoencaDAO(get_db())
            codigo = dao.Inserir(usuariodoenca)

            if codigo != None:
                flash("Estado de saúde cadastrado com sucesso!", "success")
            else:
                flash("Erro ao cadastrar estado de saúde!", "danger")

    else:
        if request.method == 'POST':
            doenca_id = request.form['doenca_id']
            usuariodoenca = UsuarioDoenca(doenca_id, usuario_codigo)

            print(usuario_codigo)
            print(doenca_id)

            dao = UsuarioDoencaDAO(get_db())
            codigo = dao.Inserir(usuariodoenca)

            if codigo != None:
                flash("Estado de saúde cadastrado com sucesso!", "success")
            else:
                flash("Erro ao cadastrar estado de saúde!", "danger")

    return render_template("historico_doencas.html", titulo="Histórico de saúde", usuario_nivel=usuario_nivel)


@app.route('/listar_doencas', methods=['GET',])
def listar_doencas():
    dao = UsuarioDoencaDAO(get_db())

    informacoes_usuario = session.get('logado')
    usuario_nivel = informacoes_usuario['nivel_usuario']
    usuario_codigo = informacoes_usuario['codigo']

    if usuario_nivel == 1:
        historico_db = dao.Listar(None, None)
        print(historico_db)
        return render_template("historico_doencas.html", historico = historico_db, usuario_nivel = usuario_nivel)
    else:
        historico_usuario = dao.Listar(usuario_codigo, None)
        print(historico_usuario)
        return render_template("historico_doencas.html", historico = historico_usuario, usuario_nivel = usuario_nivel)


# Funções de READ

@app.route('/listar_usuario', methods=['GET',])
def listar_usuario():
    dao = UsuarioDAO(get_db())

    informacoes_usuario = session.get('logado')
    usuario_nivel = informacoes_usuario['nivel_usuario']
    usuario_codigo = informacoes_usuario['codigo']

    if usuario_nivel == 1:
        usuarios_db = dao.Listar(None, None)
        return render_template("listar_usuario.html", usuarios=usuarios_db, usuario_nivel = usuario_nivel)
    else:
        usuarios_db = dao.Listar(usuario_codigo, "Listagem_individual")
        return render_template("listar_usuario.html", usuarios=usuarios_db, usuario_nivel = usuario_nivel)



@app.route('/solicitacoes', methods=['GET',])
def listar_solicitacoes():
    dao = SolicitacaoDAO(get_db())

    informacoes_usuario = session.get('logado')
    usuario_codigo = informacoes_usuario['codigo']

    solicitacoes_db = dao.Listar_Solicitacoes(usuario_codigo, None)

    solicitacoes_usuario = dao.Listar_Solicitacoes(usuario_codigo, "Individual")
    return render_template("solicitacoes.html", solicitacoes=solicitacoes_db, solicitacoes_usuario = solicitacoes_usuario)


@app.route('/doacoes_busca' , methods=['GET','POST'])
def doacoes_busca():
    dao = DoacaoDAO(get_db())
    if request.method == 'POST':
        termo = request.form['termo']

    informacoes_usuario = session.get('logado')
    usuario_codigo = informacoes_usuario['codigo']

    doacoes_db = dao.Busca_avancada(termo, None, None)
    doacoes_usuario = dao.Busca_avancada(termo, usuario_codigo , 'Individual')
    print(doacoes_db)
    return render_template("doacoes.html", doacoes=doacoes_db, doacoes_usuario = doacoes_usuario)


@app.route('/doacoes', methods=['GET',])
def doacoes():
    dao = DoacaoDAO(get_db())

    informacoes_usuario = session.get('logado')
    usuario_nivel = informacoes_usuario['nivel_usuario']
    usuario_codigo = informacoes_usuario['codigo']
    print(usuario_codigo)

    if usuario_nivel == 1:
        doacoes_db = dao.Listar(None)
        return render_template("doacoes.html", doacoes=doacoes_db, usuario_nivel = usuario_nivel)
    else:
        doacoes_db = dao.Listar(usuario_codigo)
        return render_template("doacoes.html", doacoes_usuario=doacoes_db, usuario_nivel=usuario_nivel)


@app.route('/listar_doacoes_por_data', methods=['GET',])
def listar_doacoes_por_data():
    dao = DoacaoDAO(get_db())
    doacoes_db = dao.Listar_por_data()
    return render_template("doacao_por_data.html", doacao=doacoes_db)


# Funções de UPDATE

@app.route('/atualizar_usuario, <codigo>', methods=['GET', 'POST'])
def atualizar_usuario(codigo):
    print(codigo)
    dao = UsuarioDAO(get_db())

    if request.method == "POST":
        nome = request.form['nome']
        email = request.form['email']
        cpf = request.form['cpf']
        cep = request.form['cep']
        cidade = request.form['cidade']
        dt_nasc = request.form['dt_nasc']
        tipo_sanguineo = request.form['tipo_sanguineo']
        peso = request.form['peso']
        telefone = request.form['telefone']
        opcao_doacao = request.form['opcao_doacao']
        senha = request.form['senha']

        usuario = Usuario(cpf, nome, dt_nasc, peso, tipo_sanguineo, cep, cidade, email, senha, telefone, opcao_doacao)
        usuario.setCodigo(codigo)
        ret = dao.Atualizar(usuario)

        if ret > 0:
            flash("Atualização concluída com sucesso! Código %d" % ret, "success")
        else:
            flash("Erro ao atualizar!", "danger")


    usuario_db = dao.Listar(codigo, "Checagem_individual")
    vartitulo = "Atualizar_usuario"
    return render_template("atualizar_usuario.html", titulo=vartitulo, usuario = usuario_db)


@app.route('/atualizar_solicitacao, <codigo>', methods=['GET', 'POST'])
def atualizar_solicitacao(codigo):
    dao = SolicitacaoDAO(get_db())

    if request.method == "POST":
        data = request.form['data']
        urgencia = request.form['urgencia']
        local_internacao = request.form['local_internacao']
        usuario_codigo = request.form['usuario_codigo']
        situacao = request.form['situacao']

        solicitacao = Solicitacao(data, urgencia, local_internacao, situacao, usuario_codigo)
        solicitacao.setId(codigo)

        ret = dao.Atualizar(solicitacao)

        if ret > 0:
            flash("Atualização concluída com sucesso! Código %d" % ret, "success")
        else:
            flash("Erro ao atualizar!", "danger")

    solicitacao_db = dao.Listar(codigo)
    return render_template("atualizar_solicitacao.html", solicitacao=solicitacao_db)


# Funções de DELETE

@app.route('/excluir_solicitacao/<codigo>', methods=['GET',])
def excluir_solicitacao(codigo):
    dao = SolicitacaoDAO(get_db())
    ret = dao.Excluir(codigo)
    if ret == 1:
        flash(f"Solicitação {codigo} excluída com sucesso!", "success")
    else:
        flash(f"Erro ao excluir solicitação {codigo}.", "danger")
    return redirect(url_for('listar_solicitacoes'))


@app.route('/excluir_usuario/<codigo>', methods=['GET',])
def excluir_usuario(codigo):
    dao = UsuarioDAO(get_db())
    ret = dao.Excluir(codigo)
    if ret == 1:
        flash(f"Conta excluída com sucesso!", "success")
    else:
        flash(f"Erro ao excluir Conta.", "danger")
    return redirect(url_for('logout'))


@app.route('/excluir_doenca/<codigo>', methods=['GET',])
def excluir_doenca(codigo):
    dao = UsuarioDoencaDAO(get_db())
    ret = dao.Excluir(codigo)
    if ret == 1:
        flash(f"Estado de saúde {codigo} excluído com sucesso!", "success")
    else:
        flash(f"Erro ao excluir estado de saúde{codigo}.", "danger")
    return redirect(url_for('atualizar_usuario.html'))



# Funções novas


# Função de Doar a partir da solicitação
@app.route('/doar_solicitacao, <int:codigo> <local_destino>', methods=['GET', 'POST'])
def doar_solicitacao(codigo, local_destino):


    data = date.today()
    solicitacao_codigo = codigo

    informacoes_usuario = session.get('logado')
    usuario_codigo = informacoes_usuario['codigo']

    dao = DoacaoDAO(get_db())
    dao1 = SolicitacaoDAO(get_db())
    dao2 = UsuarioDAO(get_db())
    dao3 = UsuarioDoencaDAO(get_db())

    # Obtenção/Verificação das informações compativéis

    solicitacao = dao1.Listar_Solicitacoes(solicitacao_codigo, "Verificacao")
    solicitacao = solicitacao[0]
    informacoes_solicitacao = list(solicitacao)
    informacoes_solicitacao[1] = str(informacoes_solicitacao[1])
    print(informacoes_solicitacao)

    usuario_doador = dao2.Listar(usuario_codigo, "Checagem_individual")
    informacoes_doador = list(usuario_doador)
    informacoes_doador[3] = str(informacoes_doador[3])
    print(informacoes_doador)

    historico_situacao = dao3.Listar(usuario_codigo, "verificar")
    print(historico_situacao)

    lista_data = dao.Checar_ultimadoacao(usuario_codigo)
    print(lista_data)

    if informacoes_doador[5] == informacoes_solicitacao[4] and informacoes_solicitacao[5] == "Pendente" and \
            informacoes_doador[4] >= 60 and historico_situacao == None and lista_data != None:
        doacao = Doacao(data, local_destino, solicitacao_codigo, usuario_codigo)
        codigo, email = dao.Inserir(doacao)

        if codigo > 0:
            flash("Doação cadastrada com sucesso! Código %d" % codigo, "success")
            titulo = "Solicitação atendida."
            informe = "Caro usuário, sua solicitação acaba de ser atendida. Consulte a agência a qual você está vinculado."

            notificar(email, titulo, informe)
        else:
            flash("Erro ao cadastrar doação! Verifique as informações novamente. Provavelmente você não cumpre os requisitos para satisfazer a doação.", "danger")
    else:
        flash("Você não cumpre com os requisitos básicos para doar.", "danger")

    return redirect(url_for("doar"))


# Função de Notificação

@app.route('/notificar',  methods=['GET', 'POST'])
def notificar(usuario_email, titulo, mensagem):
    email_inicial = 'maissanguetestes@gmail.com'
    senha_email = 'xmfxugkbdnekwxkq'
    email_destinatario = usuario_email

    titulo = titulo
    mensagem = mensagem

    em = EmailMessage()
    em['From'] = email_inicial
    em['To'] = email_destinatario
    em['Subject'] = titulo
    em.set_content(mensagem)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_inicial, senha_email)
        smtp.sendmail(email_inicial, email_destinatario, em.as_string())


# Função de login com Google
@app.route('/login_google')
def login_google():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        'client_secret.json',
        scopes=['https://www.googleapis.com/auth/userinfo.email','https://www.googleapis.com/auth/userinfo.profile', 'openid'])

    flow.redirect_uri = 'http://localhost/retorno'

    authorization_url, state = flow.authorization_url(access_type='offline', include_granted_scopes='true')

    #return flask.redirect(authorization_url)
    return redirect(authorization_url)

@app.route('/retorno')
def retorno():
    state = request.args.get('state')
    code = request.args.get('code')

    if code is None or code =='':
        flash("Erro ao logar com conta do google.", "danger")
        return redirect(url_for('login'))


    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        'client_secret.json',
        scopes=['https://www.googleapis.com/auth/userinfo.email','https://www.googleapis.com/auth/userinfo.profile', 'openid'],
        state=state)
    flow.redirect_uri = url_for('retorno', _external=True)

    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials

    resposta_api = requests.get('https://www.googleapis.com/oauth2/v1/userinfo?alt=json&access_token=' + credentials.token)
    info_usuario = resposta_api.json()

    email_busc = str(info_usuario['email'])
    print((info_usuario['email']))

    dao = UsuarioDAO(get_db())

    user = dao.Buscar_email(email_busc)

    if user is None:
        hash = hashlib.sha512()
        senha = os.urandom(50)
        secret = app.config['SECRET_KEY']
        hash.update(f'{secret}{senha}'.encode('utf-8'))
        senha_criptografada = hash.hexdigest()

        usuario = Usuario("", info_usuario['name'], "", "", "", "", "", info_usuario['email'], senha_criptografada, 0, "", "", "", "")

        id = None

        if usuario.nome and usuario.email and usuario.senha:
            id = dao.Inserir(usuario)

        if id is None or id <= 0:
            flash("Erro ao cadastrar usuário.", "danger")
            return redirect(url_for("login"))
        else:
            user = dao.autenticar(usuario.email, usuario.senha)

    session['logado'] = {
        'codigo': user[0],
        'cpf': user[1],
        'nome': user[2],
        'tipo_sanguineo': user[5],
        'email': user[8],
        'nivel_usuario': user[13],
        'estado_sessao': user[14]
    }


    revoke = requests.post('https://oauth2.googleapis.com/revoke',
                               params={'token': credentials.token},
                               headers={'content-type': 'application/x-www-form-urlencoded'})
    return redirect('painel')


# Função de busca avançada por usuários

@app.route('/usuarios_busca' , methods=['GET','POST'])
def usuarios_busca():
    dao = UsuarioDAO(get_db())
    if request.method == 'POST':
        termo = request.form['termo']

    usuarios_db = dao.Busca_avancada(termo)
    return render_template("listar_usuario.html", usuarios=usuarios_db)


# Corrigir bug relacionado ao tipo_sanguineo
@app.route('/solicitacoes_busca' , methods=['GET','POST'])
def solicitacoes_busca():
    dao = SolicitacaoDAO(get_db())
    if request.method == 'POST':
        termo = request.form['termo']

    informacoes_usuario = session.get('logado')
    usuario_codigo = informacoes_usuario['codigo']

    solicitacoes_db = dao.Busca_avancada(termo, usuario_codigo, None)
    # solicitacoes_usuario = dao.Busca_avancada(termo, usuario_codigo, 'Individual')
    solicitacoes_usuario = dao.Listar_Solicitacoes(usuario_codigo, "Individual")
    return render_template("solicitacoes.html", solicitacoes=solicitacoes_db, solicitacoes_usuario = solicitacoes_usuario)


# HOST


if __name__=='__main__':
    app.run(host="0.0.0.0", port=80, debug=True)
