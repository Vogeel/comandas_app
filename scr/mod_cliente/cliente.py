import requests
from flask import Blueprint, jsonify, render_template, request, redirect, url_for
from settings import HEADERS_API, ENDPOINT_CLIENTE
from mod_login.login import validaSessao
from funcoes import Funcoes
from mod_cliente.GerarPdf import PDF
from flask import send_file


bp_cliente = Blueprint('cliente', __name__, url_prefix="/cliente", template_folder='templates')

''' rotas dos formulários '''
@bp_cliente.route('/', methods=['GET', 'POST'])
@validaSessao
def formListaCliente():
    try:
        response = requests.get(ENDPOINT_CLIENTE, headers=HEADERS_API)
        result = response.json()

        if (response.status_code != 200):
            raise Exception(result[0])
        
        return render_template('formListaCliente.html', result=result[0])
    except Exception as e:
        return render_template('formListaCliente.html', msgErro=e.args[0])

@bp_cliente.route('/form-cliente/', methods=['POST', 'GET'])
@validaSessao
def formCliente():
    return render_template('formCliente.html')

@bp_cliente.route('/insert', methods=['GET', 'POST'])
@validaSessao
def insert():
    try:
        # dados enviados via FORM
        id_cliente = request.form['id']
        nome = request.form['nome']
        cpf = request.form['cpf']
        telefone = request.form['telefone']
        comprar_fiado = request.form['comprar_fiado']
        dia_fiado = request.form['dia_fiado']
        senha = Funcoes.Encrypt(request.form['senha'])

        # monta o JSON para envio a API
        payload = {'id_cliente': id_cliente, 'nome': nome, 'cpf': cpf, 'telefone': telefone, 'comprar_fiado': comprar_fiado, 'dia_fiado': dia_fiado, 'senha': senha }
        # executa o verbo POST da API e armazena seu retorno
        response = requests.post(ENDPOINT_CLIENTE, headers=HEADERS_API, json=payload)
        result = response.json()

        return redirect(url_for('cliente.formListaCliente', msg=result[0]))

    except Exception as e:
        return redirect(url_for('cliente.formListaCliente', msgErro=e.args[0]))
    
    
@bp_cliente.route("/form-edit-cliente", methods=['GET', 'POST'])
@validaSessao
def formEditCliente():
    try:
        # ID enviado via FORM
        id_cliente = request.form['id']
        # executa o verbo GET da API buscando somente o cliente selecionado,
        # obtendo o JSON do retorno
        response = requests.get(ENDPOINT_CLIENTE + id_cliente, headers=HEADERS_API)
        result = response.json()
        if (response.status_code != 200):
            raise Exception(result[0])
        # renderiza o form passando os dados retornados
        return render_template('formCliente.html', result=result[0])
    except Exception as e:
        return render_template('formListaCliente.html', msgErro=e.args[0])

@bp_cliente.route('/edit', methods=['GET', 'POST'])
@validaSessao
def edit():
    try:
        id_cliente = request.form['id']
        nome = request.form['nome']
        cpf = request.form['cpf']
        telefone = request.form['telefone']
        comprar_fiado = request.form['comprar_fiado']
        dia_fiado = request.form['dia_fiado']
        senha = Funcoes.Encrypt(request.form['senha'])

        payload = {'id_cliente': id_cliente, 'nome': nome, 'cpf': cpf, 'telefone': telefone, 'comprar_fiado': comprar_fiado, 'dia_fiado': dia_fiado, 'senha': senha }
        # executa o verbo PUT da API e armazena seu retorno
        response = requests.put(ENDPOINT_CLIENTE + id_cliente, headers=HEADERS_API, json=payload)
        result = response.json()
        if (response.status_code != 200 or result[1] != 200):
            raise Exception(result[0])
        return redirect(url_for('cliente.formListaCliente', msg=result[0]))
    except Exception as e:
        return render_template('formListaCliente.html', msgErro=e.args[0])
    
@bp_cliente.route('/delete', methods=['POST', 'GET'])
@validaSessao
def delete():
    try:
        # dados enviados via FORM
        id_cliente = request.form['id_cliente']
        # executa o verbo DELETE da API e armazena seu retorno
        response = requests.delete(ENDPOINT_CLIENTE + id_cliente, headers=HEADERS_API)
        result = response.json()
        if (response.status_code != 200 or result[1] != 200):
            raise Exception(result[0])
        # return redirect(url_for('funcionario.formListaFuncionario', msg=result[0]))
        return jsonify(erro=False, msg=result[0])
    except Exception as e:
    # return render_template('formListaFuncionario.html',
        return jsonify(erro=True, msgErro=e.args[0])
    
@bp_cliente.route('/pdfTodos', methods=['POST'])
@validaSessao
def pdfTodos():
    geraPdf = PDF()
    geraPdf.listaTodos()
    return send_file('pdfClientes.pdf')
