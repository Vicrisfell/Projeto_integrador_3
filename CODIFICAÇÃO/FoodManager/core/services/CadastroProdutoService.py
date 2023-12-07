from .repositories.FoodManagerRepository import FoodManagerRepository
from bson import ObjectId


class CadastroProdutoService:
    def __init__(self, repository: FoodManagerRepository) -> None:
        self.repository = repository

    def insert(self, data):
        return self.repository.insert("Produtos", **data)


class CadastroRequerenteService:
    def __init__(self, repository: FoodManagerRepository) -> None:
        self.repository = repository

    def insert(self, data):
        return self.repository.insert("Requerentes", **data)

    def update(self, data):
        return self.repository.update("Requerentes", **data)

    def delete(self, data):
        return self.repository.delete("Requerentes", **data)


class DoacaoService:
    def __init__(self, repository: FoodManagerRepository) -> None:
        self.repository = repository

    def delete(self, alimento_id):
        alimento_id = ObjectId(alimento_id)
        condicao = {"_id": alimento_id}
        produtos_collection = self.repository.get_collection("Produtos")
        produtos_collection.delete_one(condicao)
        # produtos.delete({"_id": alimento_id})
        update_query = {"$pull": {"produtos": {"_id": alimento_id}}}

        self.repository.update("Relatorio", condicao=condicao, **update_query)
