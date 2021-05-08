# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 20:55:10 2020

@author: nelson.junior
"""
import pymysql
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

class AdminJanela():
    
    def CadastrarProduto(self):
        self.cadastrar = Tk()
        self.cadastrar.title('Cadastro de produtos')
        self.cadastrar['bg'] = '#524f4f'
        
        Label(self.cadastrar, text='cadastre os produtos', bg='#524c4c', fg='white').grid(row=0, column=0, columnspan=4, padx=5, pady=5)
        
        Label(self.cadastrar, text='Nome', bg='#524f4f', fg='white').grid(row=1, column=0, columnspan=1, padx=5, pady=5)
        self.nome = Entry(self.cadastrar)
        self.nome.grid(row=1, column=1, columnspan=2, padx=5, pady=5)
        
        Label(self.cadastrar, text='Ingredientes', bg='#524f4f', fg='white').grid(row=2, column=0, columnspan=1, padx=5, pady=5)
        self.ingredientes = Entry(self.cadastrar)
        self.ingredientes.grid(row=2, column=1, columnspan=2, padx=5, pady=5)
        
        Label(self.cadastrar, text='Grupo', bg='#524f4f', fg='white').grid(row=3, column=0, columnspan=1, padx=5, pady=5)
        self.grupo = Entry(self.cadastrar)
        self.grupo.grid(row=3, column=1, columnspan=2, padx=5, pady=5)
        
        Label(self.cadastrar, text='Preço', bg='#524f4f', fg='white').grid(row=4, column=0, columnspan=1, padx=5, pady=5)
        self.preco = Entry(self.cadastrar)
        self.preco.grid(row=4, column=1, columnspan=2, padx=5, pady=5)
        
        Button(self.cadastrar, text='Cadastrar', width=15, bg='gray', relief='flat', highlightbackground='white', command=self.CadastrarProdutoBackEnd).grid(row=5, column=0, padx=5, pady=5)
        Button(self.cadastrar, text='Excluir', width=15, bg='gray', relief='flat', highlightbackground='white', command=self.RemoverCadastrosBackEnd).grid(row=5, column=1, padx=5, pady=5)
        Button(self.cadastrar, text='Atualizar', width=15, bg='gray', relief='flat', highlightbackground='white',command=self.MostrarProdutosBackEnd).grid(row=6, column=0, padx=5, pady=5)
        Button(self.cadastrar, text='Limpar Produtos', width=15, bg='gray', relief='flat', highlightbackground='white', command=self.LimparCadastrosBackEnd).grid(row=6, column=1, padx=5, pady=5)
        
        
        #Criação da area de visualização dos dados
        self.tree = ttk.Treeview(self.cadastrar, selectmode='browse', column=('column1','column2','column3','column4'), show='headings')
        
        # Cabeçalho das colunas de visualização
        self.tree.column("column1", width=200, minwidth=500, stretch=NO)
        self.tree.heading('#1', text='Nome')
        
        self.tree.column("column2", width=400, minwidth=500, stretch=NO)
        self.tree.heading('#2', text='Ingredientes')
        
        self.tree.column("column3", width=200, minwidth=500, stretch=NO)
        self.tree.heading('#3', text='Grupo')
        
        self.tree.column("column4", width=60, minwidth=500, stretch=NO)
        self.tree.heading('#4', text='Preço')
        
        self.tree.grid(row=0, column=4, padx=10, pady=10, columnspan=3, rowspan=6)
        
        self.MostrarProdutosBackEnd()
        
        self.cadastrar.mainloop()
            
    def __init__(self):
        self.root = Tk()
        self.root.title('Admin')
        self.root.geometry('500x500')
        
        Button(self.root, text='Pedidos', width=20, bg='#a7b1c2').grid(row=0, column=0, padx=10, pady=5)
        Button(self.root, text='Cadastros', width=20, bg='#7f8794',command=self.CadastrarProduto).grid(row=1, column=0, padx=10, pady=5)
        
        self.root.mainloop()

    def MostrarProdutosBackEnd(self):
        try:
            conexao = pymysql.connect(
                
                host='localhost',
                user='root',
                password='bolado@25',
                db='erp',
                charset='utf8mb4',                
                cursorclass=pymysql.cursors.DictCursor
                
            )
        except:
            print("Erro ao conectar ao banco de dados!")
            
        try:
            with conexao.cursor() as cursor:
                cursor.execute('select * from produtos')
                resultados = cursor.fetchall()
        except:
            print('erro ao fazer a consulta')
            
        self.tree.delete(*self.tree.get_children())
        
        linhaV = []
        
        for linha in resultados:
            linhaV.append(linha['nome'])
            linhaV.append(linha['ingredientes'])
            linhaV.append(linha['grupo'])
            linhaV.append(linha['preco'])
            
            self.tree.insert("", END, values=linhaV, iid=linha['id'], tag='1')
            
            linhaV.clear()
                
    def CadastrarProdutoBackEnd(self):
        nome = self.nome.get()
        ingredientes = self.ingredientes.get()
        grupo = self.grupo.get()
        preco = self.preco.get()
        
        try:
            conexao = pymysql.connect(
                
                host = 'localhost',
                user = 'root',
                password = 'bolado@25',
                db = 'erp',
                charset = 'utf8mb4',
                cursorclass = pymysql.cursors.DictCursor
            )
        except:
            print('Erro ao conectar no banco de dados')
        
        try:
            with conexao.cursor() as cursor:
                cursor.execute('insert into produtos(nome, ingredientes, grupo, preco)values(%s, %s, %s,%s)',(nome, ingredientes, grupo, preco))
                conexao.commit()
        except:
            print('Erro ao realizar a consulta')
            
        self.MostrarProdutosBackEnd()

    def RemoverCadastrosBackEnd(self):
        idDeletar = int(self.tree.selection()[0])
        
        try: # Conexão com o BD padrão 
            conexao = pymysql.connect(
                            
                host = 'localhost',
                user = 'root',
                password = 'bolado@25',
                db = 'erp',
                charset = 'utf8mb4',
                cursorclass = pymysql.cursors.DictCursor
            )
        except:
            print('Erro ao conectar no Banco de dados')
            
        try:
            with conexao.cursor() as cursor:
                cursor.execute('delete from produtos where id = {}'.format(idDeletar))
                conexao.commit()
        except:
            print('Erro ao realizar a consulta')
        
        self.MostrarProdutosBackEnd()

    def LimparCadastrosBackEnd(self):
        if messagebox.askokcancel('CUIDADO!!', 'Você deseja mesmo limpar o banco de dados?'):
        
            try: # Conexão com o BD padrão 
                conexao = pymysql.connect(
                                
                    host = 'localhost',
                    user = 'root',
                    password = 'bolado@25',
                    db = 'erp',
                    charset = 'utf8mb4',
                    cursorclass = pymysql.cursors.DictCursor
                )
            except:
                print('Erro ao conectar no Banco de dados')
            
            try:
                with conexao.cursor() as cursor:
                    cursor.execute('truncate table produtos;')
                    conexao.commit()
            except:
                print('Erro ao realizar a consulta')
            
            self.MostrarProdutosBackEnd()
                

class JanelaLogin():
    
# Verificação de Login
    def VerificaLogin(self):
        autenticado = False
        usuarioMaster = False
        
        try:
            conexao = pymysql.connect(
                
                host='localhost',
                user='root',
                password='bolado@25',
                db='erp',
                charset='utf8mb4',                
                cursorclass=pymysql.cursors.DictCursor
                
            )
        except:
            print("Erro ao conectar ao banco de dados!")
            
        usuario = self.login.get()
        senha = self.senha.get()
        
        try:
            with conexao.cursor() as cursor:
                cursor.execute('select * from cadastros')
                resultados = cursor.fetchall()
        except:
            print('Erro ao realizar a consulta')
            
        for linha in resultados:
            if usuario == linha['nome'] and senha == linha['senha']:
                if linha['nivel'] == 1:
                    usuarioMaster = False
                elif linha['nivel'] == 2:
                    usuarioMaster = True
                autenticado = True
                break
            else:
                autenticado = False
        
        if not autenticado:
            messagebox.showinfo('login', 'E-mail ou senha invalidos')
        
        if autenticado:
            self.root.destroy()
            if usuarioMaster:
                AdminJanela()
    
    # Cadastro de novos usuários no BD
    def CadastroBackEnd(self):
        codigoPadrao = '123@h' # Codigo de segurança padrão
        
        if self.codigoSeguranca.get() == codigoPadrao:
            if len(self.login.get()) <= 20:
                if len(self.senha.get()) <= 50:
                    nome = self.login.get()
                    
                    senha = self.senha.get()
                    
                    try: # Conexão com o BD padrão 
                        conexao = pymysql.connect(
                            
                            host = 'localhost',
                            user = 'root',
                            password = 'bolado@25',
                            db = 'erp',
                            charset = 'utf8mb4',
                            cursorclass = pymysql.cursors.DictCursor
                        )
                    except:
                        print('Erro ao conectar no Banco de dados')
                    
                    try:
                        with conexao.cursor() as cursor:
                            cursor.execute('insert into cadastros (nome, senha, nivel) values (%s, %s, %s)', (nome, senha, 1))
                            conexao.commit()
                        messagebox.showinfo('Cadastro', 'Usuario cadastrado com sucesso!')
                        self.root.destroy()
                    except:
                        ('Erro ao inserir dados')
                else:
                    messagebox.showwarning('Erro', 'Favor usar 50 caracteres ou menos')
            else:
                messagebox.showwarning('Erro', 'Favor usar 20 caracteres ou menos')
        else:
            messagebox.showwarning('Erro', 'Verificar código de segurança')
         
    # Layout de tela de cadastro
    def Cadastro(self):
        Label(self.root, text="Chave de segurança").grid(row=3, column=0, pady=5, padx=5)
        self.codigoSeguranca = Entry(self.root, show="*")
        self.codigoSeguranca.grid(row=3, column=1, pady=5, padx =10)
        Button(self.root, text='Confirmar cadastro', width=15, bg='blue1', command=self.CadastroBackEnd).grid(row=4, column=0, columnspan=3, pady=5,padx=10)
    
# Conexão com o banco para gerar a View
    def UpdateBackEnd(self):
        try: # Conexão com o BD padrão 
            conexao = pymysql.connect(
                            
                 host = 'localhost',
                 user = 'root',
                 password = 'bolado@25',
                 db = 'erp',
                 charset = 'utf8mb4',
                 cursorclass = pymysql.cursors.DictCursor
                 )
        except:
            print('Erro ao conectar no Banco de dados')
            
        try:
            with conexao.cursor() as cursor:
                cursor.execute('select * from cadastros')
                resultados = cursor.fetchall()
        except:
            print('Erro ao realizar a consulta')
        
            self.tree.delete(*self.tree.get_children())
         
        linhaV = []
        for linha in resultados:
            linhaV.append(linha['id'])
            linhaV.append(linha['nome'])
            linhaV.append(linha['senha'])
            linhaV.append(linha['nivel'])
                
            self.tree.insert("", END, values=linhaV, iid=linha['id'], tag='1')
                 
            self.linhaV.clear()
        


# Visualizador de cadastros
    def VisualizarCadastros(self):
        self.vc = Toplevel()
        self.vc.resizable(False, False)
        self.vc.title('Visualizar cadastros')
        
        #Criação da area de visualização dos dados
        self.tree = ttk.Treeview(self.vc, selectmode='browse', column=('column1','column2','column3','column4'), show='headings')
        
        # Cabeçalho das colunas de visualização
        self.tree.column("column1", width=40, minwidth=500, stretch=NO)
        self.tree.heading('#1', text='ID')
        
        self.tree.column("column2", width=100, minwidth=500, stretch=NO)
        self.tree.heading('#2', text='Usuário')
        
        self.tree.column("column3", width=100, minwidth=500, stretch=NO)
        self.tree.heading('#3', text='Senha')
        
        self.tree.column("column4", width=40, minwidth=500, stretch=NO)
        self.tree.heading('#4', text='Nível')
        
        self.tree.grid(row=0, column=0, padx=10, pady=10)
        
        # Chamando a função para poder visualizar os dados
        self.UpdateBackEnd() 
        
        self.vc.mainloop()

    def __init__(self):
        self.root = Tk()
        self.root.title('Login')
       
    # Criação de titulo
        Label(self.root, text="Faça o login").grid(row=0, column=0, columnspan=2)
       
        # Criação de Label e caixa de texto do usuário
        Label(self.root, text="usuário").grid(row=1, column=0)
        self.login = Entry(self.root)
        self.login.grid(row=1, column=1, padx=5, pady=5)
      
        # Criação de Label e caixa de texto para a senha
        Label(self.root, text="Senha").grid(row=2, column=0)
        self.senha = Entry(self.root, show="*")
        self.senha.grid(row=2, column=1, padx=5, pady=5)
     
        # Criação dos botões de log e cadastro
        Button(self.root, text='login', bg='green3', width=10, command=self.VerificaLogin).grid(row=5, column=0, padx=5, pady=5)
       
        Button(self.root, text='Cadastrar', bg='orange3', width=10, command=self.Cadastro).grid(row=5, column=1, padx=5, pady=5)
       
        # Criação dobotão de visualizar cadastros
        Button(self.root, text='Visualizar cadastros', bg='white', command=self.VisualizarCadastros).grid(row=6, column=0, columnspan=3, padx=5, pady=5)
       
        self.root.mainloop()

JanelaLogin()