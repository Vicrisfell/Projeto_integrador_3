from django.test import TestCase
from django.shortcuts import resolve_url as r
from django.urls import reverse


from .forms import RequerenteForm, ProdutoForm

# Create your tests here.


class cadastroProdutoTest(TestCase):
    def test_cadastro_produto(self):
        response = self.client.get("/cadastroProduto/")
        self.assertEqual(response.status_code, 200)

    def test_cadastro_produto_post(self):
        response = self.client.post(
            "/cadastroProduto/",
            {"nome": "teste", "validade": "01/01/2024", "quantidade": "10"},
        )
        self.assertEqual(response.status_code, 200)

    def test_cadastro_produto_post_invalido(self):
        response = self.client.post(
            "/cadastroProduto/",
            {"nome": "teste", "validade": "01/01/2024", "quantidade": "-10"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Quantidade não pode ser negativa")

    # teste se produto esta vencido a data tem que ser maior que a data atual
    def test_cadastro_produto_post_validade(self):
        response = self.client.post(
            "/cadastroProduto/",
            {"nome": "teste", "validade": "01/01/2020", "quantidade": "10"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, "Data de validade não pode ser anterior a data atual"
        )

    # teste se o nome contem numero pois nao e permitido
    def test_cadastro_produto_post_nome(self):
        response = self.client.post(
            "/cadastroProduto/",
            {"nome": "123", "validade": "01/01/2024", "quantidade": "10"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Nome não pode ser numerico")


class requerenteCadastroTest(TestCase):
    def test_requerente_cadastro(self):
        response = self.client.get("/cadastroRequerente/")
        self.assertEqual(response.status_code, 200)

    # cadastro correto
    def test_requerente_cadastro_post_valido(self):
        form_data = {
            "nome": "Thiago",
            "email": "thiago@hotmail.com",
            "telefone": "19998256345",
            "alimento": "Arroz",
        }
        form = RequerenteForm(data=form_data)
        self.assertTrue(form.is_valid())

    # nome, email, telefone e alimento
    def test_requerente_cadastro_post(self):
        response = self.client.post(
            "/cadastroRequerente/",
            {
                "nome": "Thiago",
                "email": "thiago@hotmail.com",
                "telefone": "19998256345",
                "alimento": "Feijao",
            },
        )
        self.assertEqual(response.status_code, 200)

    # nome nao pode conter numeros
    def test_requerente_cadastro_post_nome(self):
        response = self.client.post(
            "/cadastroRequerente/",
            {
                "nome": "123",
                "email": "thiago@hotmail.com",
                "telefone": "19998256345",
                "alimento": "Feijao",
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Nome não pode ser numerico")

    # telefone deve conter 11 numeros
    def test_requerente_cadastro_post_telefone(self):
        response = self.client.post(
            "/cadastroRequerente/",
            {
                "nome": "Thiago",
                "email": "thiago@hotmail.com",
                "telefone": "123456789",
                "alimento": "Feijao",
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Telefone deve conter 11 numeros")

    # teste email sem @ tem que dar erro


def test_requerente_cadastro_post_email(self):
    response = self.client.post(
        "/cadastroRequerente/",
        {
            "nome": "Thiago",
            "email": "thiagohotmail.com",
            "telefone": "19998256345",
            "alimento": "Feijao",
        },
        follow=True,
    )
    content = response.content.decode("utf-8")
    print(content)
    self.assertEqual(response.status_code, 200)
    self.assertIn("Email deve conter @", content)

    # teste se alimento nao pode ser numerico
    def test_requerente_cadastro_post_alimento(self):
        response = self.client.post(
            "/cadastroRequerente/",
            {
                "nome": "Thiago",
                "email": "thiagohotmail.com",
                "telefone": "19998256345",
                "alimento": "123",
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Alimento não pode ser numerico")


class IndexTest(TestCase):
    def setUp(self):
        # self.resp = self.client.get(r("core:index"), follow=True)
        self.resp = self.client.get(reverse("index"))

    def test_status_code(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, "index.html")

    def test_html(self):
        tags = (
            ("<html", 1),
            ("<head", 2),
            ("<title", 1),
            ("<body", 2),
            ("<br", 1),
            ("<button", 1),
            ("<div", 62),
        )
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.resp, text, count)
