from django.urls import path
from .views import cadastroRequerente

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("cadastroProduto/", views.cadastroProduto, name="cadastroProduto"),
    path("cadastroRequerente/", views.cadastroRequerente, name="cadastroRequerente"),
    path("listarProduto/", views.listarProdutos, name="listarProdutos"),
    path("listarRequerente/", views.listarRequerentes, name="listarRequerente"),
    path("listarConta/", views.listarConta, name="listarConta"),
    # path("index_with_total/", views.index_with_total, name="index_with_total"),
]
