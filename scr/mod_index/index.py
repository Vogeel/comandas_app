from flask import Blueprint, render_template
from mod_login.login import validaSessao
bp_index = Blueprint('index', __name__, url_prefix="/home", template_folder='templates')

''' rotas dos formulários '''
@bp_index.route('/')
@validaSessao
def formListaIndex():
    return render_template('formListaIndex.html'), 200