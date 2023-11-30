from fpdf import FPDF
from datetime import datetime
import requests

from settings import HEADERS_API, ENDPOINT_FUNCIONARIO

class PDF(FPDF):
    def header(self):
        self.image("scr/static/PdfLogo.png", 10, 8, 20)
        self.set_font('helvetica', 'B', 15)
        self.cell(0, 5, 'Seu zé', 0, 1, 'C', 0)
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.cell(0, 10, 'Página ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

    def listaTodos(self):
        pdf = PDF(orientation="P", unit="mm", format="A4") # L paisagem, P retrato
        pdf.set_author("Vitor")
        pdf.set_title('Funcionarios')
        pdf.alias_nb_pages() # mostra o número da página no rodapé
        pdf.add_page()
        # mostra o cabeçalho
        pdf.set_font('helvetica', 'b', 12)
        pdf.cell(190, 5, 'Funcionarios', 0, 1, 'C', 0)
        pdf.set_font('helvetica', '', 6)
        pdf.cell(190, 4, "Emitido em: " + str(datetime.now()), 0, 1, 'R')
        pdf.ln(5)
        # monta tabela para mostrar os dados
        pdf.set_font('helvetica', 'B', 8)
        pdf.cell(10, 5, 'ID', 0, 0, 'L')
        pdf.cell(25, 5, 'Nome', 0, 0, 'L')
        pdf.cell(15, 5, 'Matricula', 0, 0, 'L')
        pdf.cell(25, 5, 'CPF', 0, 0, 'L')
        pdf.cell(25, 5, 'Telefone', 0, 0, 'L')
        pdf.cell(15, 5, 'Grupo', 0, 1, 'L')

        # busca na API e mostra todos os dados
        pdf.set_font('helvetica', '', 8)
        try:
            response = requests.get(ENDPOINT_FUNCIONARIO, headers=HEADERS_API)
            result = response.json()
            if (response.status_code != 200):
                raise Exception(result[0])
            for row in result[0]:
                pdf.cell(10, 5, str(row['id_funcionario']), 0, 0, 'L')
                pdf.cell(25, 5, str(row['nome']), 0, 0, 'L')
                pdf.cell(15, 5, str(row['matricula']), 0, 0, 'L')
                pdf.cell(25, 5, str(row['cpf']), 0, 0, 'L')
                pdf.cell(25, 5, str(row['telefone']), 0, 0, 'L')
                pdf.cell(15, 5, str(row['grupo']), 0, 1, 'L')
        except Exception as e:
            pdf.multi_cell(190, 5, 'ERRO: ' + str(e.args[0]), 1, 'J', False)
        # baixa o relatório criado
        pdf.output('scr/pdfFuncionarios.pdf')