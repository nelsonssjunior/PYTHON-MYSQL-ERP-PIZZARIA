# -*- coding: utf-8 -*-
"""
Created on Sun Mar  8 15:23:46 2020

@author: nelson.junior
"""
import pymysql.cursors
import matplotlib.pyplot as plt


# Conexão com banco de dados
conexao = pymysql.connect(
    host='localhost',
    user='root',
    password='bolado@25',
    charset='utf8mb4',
    db='erp',
    cursorclass=pymysql.cursors.DictCursor)

autentico = False

# Função para validação e cadastro de usuários


def logarCadastrar():
    usuarioExistente = 0
    autenticado = False
    usuarioMaster = False

    if decisao == 1:   # Entradas do usuario
        nome = input('Digite seu nome :')
        senha = input('Digite sua senha :')

        for linha in resultado:   # Verificação de conta e nível de usuário
            if nome == linha['nome'] and senha == linha['senha']:
                if linha['nivel'] == 1:
                    usuarioMaster = False
                elif linha['nivel'] == 2:
                    usuarioMaster = True
                autenticado = True
                break
            else:
                autenticado = False
        if not autenticado:   # Tratando erro de input do uauário
            print('Email ou senha errado')

    elif decisao == 2:
        print('Faça seu cadastro')
        nome = input('Digite seu nome :')
        senha = input('Digite sua senha :')

        for linha in resultado:   # verificar se usuário e senha são iguais
            if nome == linha['nome'] and senha == linha['senha']:
                usuarioExistente = 1

        if usuarioExistente == 1:
            print('usuário ja cadatstrado, tente um nome e senha diferentes!')
        elif usuarioExistente == 0:
            try:
                with conexao.cursor() as cursor:
                    cursor.execute('insert into cadastros(nome, senha, nivel)'
                                   'values(%s, %s, %s)', (nome, senha, 1))
                    conexao.commit()
                print('usuario cadastrado com sucesso!')
            except:
                print('Erro ao inserir os dados')

    return autenticado, usuarioMaster

# Função cadastro de produtos no sistema


def cadastrarProdutos():
    nome = input('digite o nome do produto: ')
    ingredientes = input('digite os igredientes do produto: ')
    grupo = input('digite o grupo pertencente a esse produto: ')
    preco = float(input('digite o preço do produto: '))

    try:
        with conexao.cursor() as cursor:
            cursor.execute('insert into produtos(nome, ingredientes, grupo, preco)'
                           'values(%s,%s,%s,%s)', (nome, ingredientes, grupo, preco) )
            conexao.commit()
            print('produto cadastrado com sucesso')
    except:
        print('Erro ao inserir os produtos no banco de dados')


# Função para listar base de produtos pro usuário

def listarProdutos():
    produtos = []
    try:
        with conexao.cursor() as cursor:
            cursor.execute('select * from produtos')
            produtosCadastrados = cursor.fetchall()
            print(produtosCadastrados)
    except:
        print('erro ao conectar ao banco de dados')

    for i in produtosCadastrados:
        produtos.append(i)

    if len(produtos) != 0:
        for i in range(0, len(produtos)):
            print(produtos[i])
    else:
        print('nenhum produto cadastrado')


def excluirProduto():
    idDeletar = int(input('digite o id do produto que deseja deletar: '))

    try:
        with conexao.cursor() as cursor:
            cursor.execute('delete from produtos where id = {}'
                           .format(idDeletar))
    except:
        print('erro ao excluir produto')


def listarPedidos():
    pedidos = []
    decision = 0

    while decision != 2:
        pedidos.clear()

        try:
            with conexao.cursor as cursor:
                cursor.execute('select * from pedidos')
                listaPedidos = cursor.fetchall()
        except:
            print('erro no banco de dados')

        for i in listaPedidos:
            pedidos.append(i)

        if len(pedidos) != 0:
            for i in range(0, len(pedidos)):
                print(pedidos[i])
        else:
            print('Nenhum pedido cadastrado')

        decision = int(input('digite 1 para entregar ou 2 para voltar: '))

        if decision == 1:
            idDeletar = int(input('Digite o id do pedido entregue: '))

            try:
                with conexao.cursor() as cursor:
                    cursor.execute('delete from pedidos where id = {}'.format(idDeletar))
                    print('Pedido entregue com sucesso!')
            except:
                print('Erro ao entregar dar pedido como entregue')


def gerarEstatistica():

    nomeProdutos = []
    nomeProdutos.clear

    try:
        with conexao.cursor() as cursor:
            cursor.execute('select * from produtos')
            produtos = cursor.fetchall()
    except:
        print('erro ao fazer consulta no banco de dados')

    try:
        with conexao.cursor() as cursor:
            cursor.execute('select * from estatisticavendido')
            vendido = cursor.fetchall()
    except:
        print('erro ao fazer consulta no banco de dados')

    estado = int(input('Digite 0 para sair, 1 para pesquisar por nome e 2 para pesquisar por grupo: '))
    
    if estado == 1:
        decisao3 = int(input('Digite 1 para pesquisar por valor e 2 para grupo: '))
        if decisao3 == 1:

            for i in produtos:
                nomeProdutos.append(i['nome'])

            valores = []
            valores.clear()

            for h in range(0, len(nomeProdutos)):
                somaValor = -1
                for i in vendido:
                    if i['nome'] == nomeProdutos[h]:
                        somaValor += i["preco"]
                if somaValor == -1:
                    valores.append(0)
                elif somaValor > 0:
                    valores.append(somaValor + 1)

            plt.plot(nomeProdutos, valores)
            plt.ylabel('Quantidade vendida em reais $$$')
            plt.xlabel('produto')
            plt.show()
        
        if decisao3 == 2:
            grupoUnico = []
            grupoUnico.clear()
            
            try:
                with conexao.cursor() as cursor:
                    cursor.execute('select * from produtos')
                    grupo = cursor.fetchall()
            except:
                print('erro na consulta')
                
            try:
                with conexao.cursor() as cursor:
                    cursor.execute('select * from estatisticaVendido')
                    vendidoGrupo = cursor.fetchall()
            except:
                print('erro na consulta')
            
            for i in grupo:
                grupoUnico.append(i['nome'])
            
            grupoUnico = sorted(set(grupoUnico))
            qntFinal = []
            qntFinal.clear()
            
            for h in range(0, len(grupoUnico)):
                qntUnitaria = 0
                for i in vendidoGrupo:
                    if grupoUnico[h] == i['nome']:
                        qntUnitaria += 1
                qntFinal.append(qntUnitaria)
            plt.plot(grupoUnico, qntFinal)
            plt.ylabel('quantidade unitaria vendida')
            plt.xlabel('produtos')
            

#  Menu inicial
while not autentico:
    decisao = int(input('Digite 1 para logar e 2 para cadastrar: '))

    try:
        with conexao.cursor() as cursor:
            cursor.execute('select * from cadastros')
            resultado = cursor.fetchall()
    except:
        print('Erro ao conectar no banco de dados')

# Validação de admin para cadastro de produtos
    autentico, usuarioSupremo = logarCadastrar()

if autentico:
    print('Autenticado')

    if usuarioSupremo == True:
        decisaoUsuario = 1

        while decisaoUsuario != 0:
            decisaoUsuario = int(input('digite 0 pra sair, 1 para cadastrar produtos, 2 para listar produtos cadastrados, '
                                       '3 para listar pedidos e 4 para verificar os dados: '))
            if decisaoUsuario == 0:
                print('Programa finalizado!')
            if decisaoUsuario == 1:
                cadastrarProdutos()
            if decisaoUsuario == 2:
                listarProdutos()
                delete = int(input('digite 1 para excluir um produto ou 2 para sair: '))

                if delete == 1:
                    excluirProduto()
                    
            if decisaoUsuario == 3:
                listarPedidos()
                
            if decisaoUsuario == 4:
                gerarEstatistica()