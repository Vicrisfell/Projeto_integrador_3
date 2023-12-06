from django.shortcuts import render, redirect
from .forms import ProdutoForm, RequerenteForm
from .services.ConnectionService import ConnectionService
from .services.MongoServie import MongoService
from .services.repositories.FoodManagerRepository import FoodManagerRepository
from .services.CadastroProdutoService import (
    CadastroProdutoService,
    CadastroRequerenteService,
)

# log

import logging


# Create your views here.


def index(request):
    return render(request, "index.html")


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
        else:
            return render(request, "cadastroProduto.html", {"form": form})
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


# def listarProdutos(request):
#     conexao = ConnectionService()
#     mongo = MongoService(conexao, "FoodManager")
#     repository = FoodManagerRepository(mongo)
#     produtos = list(repository.find("Produtos", **{}))
#     return render(request, "listarProdutos.html", {"produtos": produtos})


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

    # Obter todos os produtos
    produtos = list(repository.find("Produtos", **{}))

    # Filtrar produtos em estoque com quantidade acima de 1
    produtos_disponiveis = [produto for produto in produtos if produto["quantidade"] > 1]

    # Obter a lista de nomes dos produtos disponíveis
    nomes_produtos_disponiveis = [produto["nome"] for produto in produtos_disponiveis]

    # Verificar se o formulário foi submetido
    if request.method == "POST":
        # Obter o nome do alimento selecionado no formulário
        alimento_selecionado = request.POST.get("alimento")

        # Restante do código para processar o formulário...

    # Passar a lista de produtos disponíveis para o template
    return render(
        request,
        "doacao.html",
        {"produtos_disponiveis": produtos_disponiveis, "nomes_produtos_disponiveis": nomes_produtos_disponiveis},
    )


# def get_total_products():
#     # Conectar ao MongoDB
#     conexao = ConnectionService()
#     mongo = MongoService(conexao, "FoodManager")
#     repository = FoodManagerRepository(mongo)

#     # Obter a coleção de produtos
#     produtos_collection = repository.get_collection("Produtos")

#     # Agregação para obter o total de produtos
#     total_products_aggregation = [
#         {"$group": {"_id": None, "totalQuantidade": {"$sum": "$quantidade"}}}
#     ]

#     total_products_result = list(
#         produtos_collection.aggregate(total_products_aggregation)
#     )

#     # Retornar o total de produtos (ou 0 se não houver resultados)
#     total_products = (
#         total_products_result[0]["totalQuantidade"] if total_products_result else 0
#     )

#     return total_products


# def index_with_total(request):
#     total_produtos = get_total_products()
#     return render(request, "index.html", {"total_produtos": total_produtos})
