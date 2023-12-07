from django.urls import path
from .views import cadastroRequerente

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("cadastroProduto/", views.cadastroProduto, name="cadastroProduto"),
    path("cadastroRequerente/", views.cadastroRequerente, name="cadastroRequerente"),
    path("listarProdutos/", views.listarProdutos, name="listarProdutos"),
    path("listarRequerente/", views.listarRequerentes, name="listarRequerente"),
    path("listarConta/", views.listarConta, name="listarConta"),
    path("cadastroDoacao/", views.cadastroDoacao, name="cadastroDoacao"),
    path(
        "remover_alimento/<str:alimento_id>/",
        views.remover_alimento,
        name="remover_alimento",
    ),
    # path("index_with_total/", views.index_with_total, name="index_with_total"),
]
