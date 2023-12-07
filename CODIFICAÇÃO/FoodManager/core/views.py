from django.shortcuts import render, redirect
from django import forms
from .forms import DoacaoForm, ProdutoForm, RequerenteForm
from .services.ConnectionService import ConnectionService
from .services.MongoServie import MongoService
from .services.repositories.FoodManagerRepository import FoodManagerRepository
from .services.CadastroProdutoService import (
    CadastroProdutoService,
    CadastroRequerenteService,
    DoacaoService,
)

# log

import logging


# Create your views here.


def index(request):
    #renderizacao da pesquisa na collection produtos 
    conexao = ConnectionService()
    mongo = MongoService(conexao, "FoodManager")
    repository = FoodManagerRepository(mongo)
    produtos = list(repository.find("Produtos", **{}))
    return render(request, "index.html", {"produtos": produtos})




def cadastroProduto(request):
    if request.method == "POST":
        form = ProdutoForm(request.POST)
        if form.is_valid():
            conexao = ConnectionService()
            mongo = MongoService(conexao, "FoodManager")
            repository = FoodManagerRepository(mongo)
            service = CadastroProdutoService(repository)
            service.insert(form.cleaned_data)
            return redirect("cadastroProduto")
            produtos = list(repository.find("Produtos", **{}))
        else:
            return render(request, "cadastroProduto.html", {"form": form, 'produtos': produto})
    form = ProdutoForm()
    return render(request, "cadastroProduto.html", {"form": form})


# cadastro de requerentes
def cadastroRequerente(request):
    if request.method == "POST":
        form = RequerenteForm(request.POST)
        if form.is_valid():
            conexao = ConnectionService()
            mongo = MongoService(conexao, "FoodManager")
            repository = FoodManagerRepository(mongo)
            service = CadastroRequerenteService(repository)
            service.insert(form.cleaned_data)
        else:
            return render(request, "cadastroRequerente.html", {"form": form})
    form = RequerenteForm()
    return render(request, "cadastroRequerente.html", {"form": form})


def listarRequerentes(request):
    conexao = ConnectionService()
    mongo = MongoService(conexao, "FoodManager")
    repository = FoodManagerRepository(mongo)
    requerentes = list(repository.find("Requerentes", **{}))
    return render(request, "listarRequerentes.html", {"requerentes": requerentes})


def listarConta(request):
    conexao = ConnectionService()
    mongo = MongoService(conexao, "FoodManager")
    repository = FoodManagerRepository(mongo)
    conta = list(repository.find("Conta", **{}))
    return render(request, "listarConta.html", {"conta": conta})


# buscar ultimo registro no mongo
def buscarUltimoRegistro(request):
    conexao = ConnectionService()
    mongo = MongoService(conexao, "FoodManager")
    # repository = FoodManagerRepository(mongo)
    collection = mongo.db["Produtos"]
    print(collection)
    ultimoRegistro = collection.find_one({}, sort=[("_id", -1)])
    # logging.basicConfig(filename="log.txt", level=logging.INFO)
    logging.info(f"Ultimo Registro: {ultimoRegistro}")
    return render(request, "index.html", {"ultimoRegistro": ultimoRegistro})


def listarProdutos(request):
    # Conectar ao MongoDB
    conexao = ConnectionService()
    mongo = MongoService(conexao, "FoodManager")
    repository = FoodManagerRepository(mongo)

    # Obter todos os produtos
    produtos = list(repository.find("Produtos", **{}))

    # Calcular a quantidade total
    quantidade_total = sum([produto["quantidade"] for produto in produtos])

    # Imprimir o conteúdo de produtos e a quantidade total para depuração
    print("Produtos:", produtos)
    print("Quantidade Total:", quantidade_total)

    # Passar os produtos e a quantidade total para o template
    return render(
        request,
        "listarProdutos.html",
        {"produtos": produtos, "quantidade_total": quantidade_total},
    )


# Minha colection de produtos
# _id 656f085fc0dd6e7dd306906c
# nome "Feijão"
# quantidade 5
# validade 2023-12-31T00:00:00.000+00:00
def cadastroDoacao(request):
    # Conectar ao MongoDB
    conexao = ConnectionService()
    mongo = MongoService(conexao, "FoodManager")
    repository = FoodManagerRepository(mongo)
    print(conexao)
    # Obter todos os produtos
    produtos = list(repository.find("Produtos", **{}))

    # Filtrar produtos em estoque com quantidade acima de 1
    produtos_disponiveis = [
        produto for produto in produtos if produto["quantidade"] > 1
    ]

    # Obter a lista de nomes dos produtos disponíveis
    nomes_produtos_disponiveis = [produto["nome"] for produto in produtos_disponiveis]
    print(nomes_produtos_disponiveis)

    # Verificar se o formulário foi submetido
    if request.method == "POST":
        # Obter o nome do alimento selecionado no formulário
        alimento = request.POST.get("nomes_produtos_disponiveis")
        print(alimento)
        # Restante do código para processar o formulário...

    # Passar a lista de produtos disponíveis para o template
    return render(
        request,
        "cadastroRequerente.html",
        # "doacao.html",
        {
            "form": DoacaoForm(),
            "produtos_disponiveis": produtos_disponiveis,
            "nomes_produtos_disponiveis": nomes_produtos_disponiveis,
        },
    )

#remover alimento              
def remover_alimento(request,alimento_id):
    # Conectar ao MongoDB
    conexao = ConnectionService()
    mongo = MongoService(conexao, "FoodManager")
    repository = FoodManagerRepository(mongo)
    alimento_id = ObjectId(alimento_id)
    repository.delete("Produtos",alimento_id)
    return redirect('listarProdutos')


    # alimento_id = ObjectId(alimento_id)
    # connection = ConexaoService()
    # bd = MongoConnectionService(connection,"FoodShare")
    # repository = FoodShareRepository(bd)
    # doacao = DoacaoService(repository)
    # doacao.delete(alimento_id,request.session.get('user_id'))
    # doacao.__del__
    # return redirect('relatorio')