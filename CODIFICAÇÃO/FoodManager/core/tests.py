from django.test import TestCase

# Create your tests here.


class cadastroProdutoTest(TestCase):
    def test_cadastro_produto(self):
        response = self.client.get("/cadastroProduto/")
        self.assertEqual(response.status_code, 200)
