from flask import Blueprint, render_template, request, redirect, url_for
from funcoes import Funcoes
from settings import HEADERS_API, ENDPOINT_FUNCIONARIO
import requests



bp_funcionario = Blueprint('funcionario', __name__, url_prefix="/funcionario", template_folder='templates')

''' rotas dos formulários '''
@bp_funcionario.route('/', methods=['GET', 'POST'])
def formListaFuncionario():
    try:
        response = requests.get(ENDPOINT_FUNCIONARIO, headers=HEADERS_API)
        result = response.json()

        if (response.status_code != 200):
            raise Exception(result[0])
        
        return render_template('formListaFuncionario.html', result=result[0])
    except Exception as e:
        return render_template('formListaFuncionario.html', msgErro=e.args[0])

@bp_funcionario.route('/form-funcionario/', methods=['POST', 'GET'])
def formFuncionario():
    return render_template('formFuncionario.html')

@bp_funcionario.route('/insert', methods=['POST'])
def insert():
    try:
        # dados enviados via FORM
        id_funcionario = request.form['id']
        nome = request.form['nome']
        matricula = request.form['matricula']
        cpf = request.form['cpf']
        telefone = request.form['telefone']
        grupo = request.form['grupo']
        senha = Funcoes.Encrypt(request.form['senha'])

        # monta o JSON para envio a API
        payload = {'id_funcionario': id_funcionario, 'nome': nome, 'matricula': matricula, 'cpf': cpf, 'telefone': telefone, 'grupo': grupo, 'senha': senha}
        
        # executa o verbo POST da API e armazena seu retorno
        response = requests.post(ENDPOINT_FUNCIONARIO, headers=HEADERS_API, json=payload)
        result = response.json()
        
        print(result) # [{'msg': 'Cadastrado com sucesso!', 'id': 13}, 200]
        print(response.status_code) # 200
        
        if (response.status_code != 200 or result[1] != 200):
            raise Exception(result[0])
        
        return redirect(url_for('funcionario.formListaFuncionario', msg=result[0]))

    except Exception as e:
        return redirect(url_for('funcionario.formListaFuncionario', msgErro=e.args[0]))

