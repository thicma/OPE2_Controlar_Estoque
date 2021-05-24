from fpdf import FPDF
from estoque.models import *
from datetime import *

# create FPDF object
# Layout ('P', 'L')
# Unit ('mm','cm', 'in')
# format ('a3', a4 (default), A5, 'Letter', 'Legal', (100,150)
title = 'Relatório de movimentação financeira ForU'
class PDF(FPDF):
    def header(self):
        #logo
        self.image('logo_ForU_Login.png', 10, 10, 50)
        #font
        self.set_font('helvetica', 'B', 20)
        title_w = self.get_string_width(title)
        doc_w = self.w
        self.set_x(((doc_w - title_w) / 2) + 70)
        #title
        self.cell(30,30, title, ln=1, align='C')
        # line break

        #self.ln(20)
    
    def footer(self):
        #set position of the footer
        self.set_y(-15)
        #set font
        self.set_font('helvetica', 'I', 10)
        # Page number
        self.cell(0,10, f'Page {self.page_no()}/{{nb}}', align='C')
    
    def body(self, lista_resultados):
        #get total pages numbers
        self.alias_nb_pages()
        #adiciona páginas
        self.add_page()
        self.set_font('helvetica', 'BI', 12)
        self.cell(70,10,'Produto', border=True)
        self.cell(70,10,'Marca', border=True)
        self.cell(20,10,'Data', border=True)
        self.cell(20,10,'Qtde', border=True)
        self.cell(20,10,'Valor', border=True)
        self.cell(60,10,'Tipo da Movimentação', border=True, ln=True)        
        self.set_font('helvetica', '', 10)
        for linha in lista_resultados:
            self.cell(70,10, f'{linha.produto.descricao.title()}', border=True)
            self.cell(70,10,f'{linha.produto.marca.nome.title()}', border=True)
            self.cell(20,10,f"{linha.data.strftime('%d/%m/%Y')}", border=True)
            self.cell(20,10,f'{linha.quantidade}', border=True)
            self.cell(20,10,f'R${linha.valor:.2f}', border=True)
            self.cell(60,10,f'{linha.tipo_movimentacao.title()}', border=True, ln=True)
        
        nome_do_arquivo = f"C:/Users/HeJuThBb/Documents/GitHub/OPE2_Controlar_Estoque/EstoqueForU/estoque/static/client/pdf/ForU_{datetime.now().strftime('%d-%m-%Y_%H-%M-%S')}.pdf"
        
        self.output(nome_do_arquivo, 'F')
        return f"ForU_{datetime.now().strftime('%d-%m-%Y_%H-%M-%S')}.pdf"




#set auto page break
#pdf.set_auto_page_break(auto=True, margin=10)

#get total pages numbers
#pdf.alias_nb_pages()

#pdf.add_page()
# specify font
# fonts (times, courier, helvetica, symbol, zpfdingbats)
#B (bold), U (underline), I italics, '' regular, combination (i.e, ('BU'))


# w = width
# h = heigth
# txt = your text
# ln (0 False; 1 True - move cursor down to next line)
# border (0 False; 1 True - add border around cell)


"""    
for x in range (1, 41):
    pdf.cell(40,10,f' This is line {x}', ln=1)
"""
#multi_cell serve para quebrar linha

#pdf.output('pd_1.pdf')

