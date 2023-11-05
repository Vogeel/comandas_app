import requests
from flask import Blueprint, render_template, request, redirect, url_for
from settings import HEADERS_API, ENDPOINT_PRODUTO
import base64


bp_produto = Blueprint('produto', __name__, url_prefix="/produto", template_folder='templates')

''' rotas dos formulários '''
@bp_produto.route('/', methods=['GET', 'POST'])
def formListaProduto():
    try:
        response = requests.get(ENDPOINT_PRODUTO, headers=HEADERS_API)
        result = response.json()

        if (response.status_code != 200):
            raise Exception(result[0])
        
        return render_template('formListaProduto.html', result=result[0])
    except Exception as e:
        return render_template('formListaProduto.html', msgErro=e.args[0])

@bp_produto.route('/form-produto/', methods=['POST', 'GET'])
def formProduto():
    return render_template('formProduto.html')

@bp_produto.route('/insert', methods=['POST'])
def insert():
    try:
        # dados enviados via FORM
        id_produto = request.form['id']
        nome = request.form['nome']
        descricao = request.form['descricao']
        valor_unitario = request.form['valor_unitario']
        foto = "data:" + request.files['foto'].content_type + ";base64," + str(base64.b64encode(request.files['foto'].read()), "utf-8")

        # monta o JSON para envio a API
        payload = {'id_produto': id_produto, 'nome': nome, 'descricao': descricao, 'foto': foto, 'valor_unitario': valor_unitario }
        
        # executa o verbo POST da API e armazena seu retorno
        response = requests.post(ENDPOINT_PRODUTO, headers=HEADERS_API, json=payload)
        result = response.json()
        
        
        return redirect(url_for('produto.formListaProduto', msg=result[0]))

    except Exception as e:
        return redirect(url_for('formListaProduto.html', msgErro=e.args[0]))
    
    
@bp_produto.route("/form-edit-produto", methods=['POST'])
def formEditProduto():
    try:
        id_produto = request.form['id']
        response = requests.get(ENDPOINT_PRODUTO + id_produto, headers=HEADERS_API)
        result = response.json()
        if (response.status_code != 200 or result[1] != 200):
            raise Exception(result[0])
        return render_template('formProduto.html', result=result[0])
    except Exception as e:
        return render_template('formListaProduto.html', msgErro=e.args[0])

@bp_produto.route('/edit', methods=['POST'])
def edit():
    try:
            id_produto = request.form['id']
            nome = request.form['nome']
            descricao = request.form['descricao']
            valor_unitario = request.form['valor_unitario']
            foto = "data:" + request.files['foto'].content_type + ";base64," + str(
                base64.b64encode(request.files['foto'].read()), "utf-8")

            payload = {
                'id_produto': id_produto,
                'nome': nome,
                'descricao': descricao,
                'foto': foto,
                'valor_unitario': valor_unitario
            }

            response = requests.put(
                ENDPOINT_PRODUTO + id_produto, headers=HEADERS_API, json=payload)
            result = response.json()

            if (response.status_code != 200 or result[1] != 201):
                raise Exception(result[0])

            return redirect(url_for('produto.formListaProduto', msg=result[0]))

    except Exception as e:
            return render_template('formListaProduto.html', msgErro=e.args[0])