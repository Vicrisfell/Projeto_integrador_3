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


def listarProdutos(request):
    conexao = ConnectionService()
    mongo = MongoService(conexao, "FoodManager")
    repository = FoodManagerRepository(mongo)
    produtos = list(repository.find("Produtos", **{}))
    return render(request, "listarProdutos.html", {"produtos": produtos})


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
