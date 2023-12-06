from django.shortcuts import render, redirect
from .forms import ProdutoForm, RequerenteForm, DoadorForm
from .models import Produto
from .services.ConnectionService import ConnectionService
from .services.MongoServie import MongoService
from bson import ObjectId
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
    # conexao = ConnectionService()
    # mongo = MongoService(conexao, "FoodManager")
    # repository = FoodManagerRepository(mongo)
    # # Obter a coleção de produtos
    # produtos_collection = list(repository.find("Produtos", **{}))
    # # Buscar o produto pelo nome
    # produto = list(repository.find("Produtos", **{}))
    # # Atualizar a quantidade do produto
    # return render(request, "doacao.html")
    def cadastroDoacao(request):
        if request.method == "POST":
            form = DoadorForm(request.POST)
            if form.is_valid():
                # Obtenha os dados do formulário
                escolha_alimento = form.cleaned_data["alimento"]

                # Conectar ao MongoDB
                conexao = ConnectionService()
                mongo = MongoService(conexao, "FoodManager")
                repository = FoodManagerRepository(mongo)
                collection = mongo.db["Produtos"]

                # Obter o produto escolhido
                produto = collection.find_one(
                    "Produtos", {"_id": ObjectId(escolha_alimento)}
                )

                # Criar uma nova doação
                nova_doacao = Produto(
                    alimento=produto["nome"],
                    quantidade=1,  # Ajuste conforme necessário
                    validade=produto["validade"],
                    # Adicione outros campos conforme necessário
                )

                # Salvar a doação no banco de dados
                collection.insert(nova_doacao, "Doacoes")

                # Atualizar a quantidade do produto, se necessário
                # Certifique-se de ajustar conforme necessário com a lógica específica

                return redirect(
                    "listarProdutos"
                )  # Redirecionar para a página de sucesso após a doação

        else:
            form = DoadorForm()

        return render(request, "doacao.html", {"form": form})
