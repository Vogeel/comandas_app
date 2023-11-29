from flask import Blueprint, render_template, request, redirect, url_for, session
from functools import wraps
from funcoes import Funcoes
bp_login = Blueprint('login', __name__, url_prefix='/', template_folder='templates')
@bp_login.route("/", methods=['GET', 'POST'])
def login():
    return render_template("formLogin.html")

@bp_login.route('/login', methods=['POST'])
def validaLogin():
    try:
        # dados enviados via FORM
        cpf = request.form['usuario']
        senha = Funcoes.Encrypt(request.form['senha'])
        # limpa a sessão
        session.clear()
        if (cpf == "abc" and senha == Funcoes.Encrypt('Bolinhas')):
            # registra usuário na sessão, armazenando o login do usuário
            session['login'] = cpf
            # abre a aplicação na tela home
            return redirect(url_for('index.formListaIndex'))
        else:
            raise Exception("Falha de Login! Verifique seus dados e tente novamente!")

    except Exception as e:
        # retorna para a tela de login
        return redirect(url_for('login.login', msgErro=e.args[0]))
    
@bp_login.route("/logoff", methods=['GET'])
def logoff():
    # limpa um valor individual
    session.pop('login', None)
    # limpa toda sessão
    session.clear()
    # retorna para a tela de login
    return redirect(url_for('login.login'))

def validaSessao(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'login' not in session:
            # descarta os dados copiados da função original e retorna a tela de login
            return redirect(url_for('login.login', msgErro='Usuário não logado!'))
        else:
            # retorna os dados copiados da função original
            return f(*args, **kwargs)
    # retorna o resultado do if acima
    return decorated_function