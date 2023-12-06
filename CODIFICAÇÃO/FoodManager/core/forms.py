from django import forms
from datetime import datetime


# produto, requerente, doador

# testes referentes a html e status


class ProdutoForm(forms.Form):
    nome = forms.CharField(max_length=100, required=True)
    quantidade = forms.IntegerField(required=True)
    # validade do produto
    validade = forms.DateField(required=True)

    # metodo validacao
    def clean_nome(self):
        nome = self.cleaned_data["nome"]
        if nome.isnumeric():
            raise forms.ValidationError("Nome não pode ser numerico")
        return nome

    def clean_quantidade(self):
        quantidade = self.cleaned_data["quantidade"]
        if quantidade < 0:
            raise forms.ValidationError("Quantidade não pode ser negativa")
        return quantidade

    def clean_validade(self):
        validade = self.cleaned_data["validade"]
        data_atual = datetime.now().date()
        if validade < data_atual:
            raise forms.ValidationError(
                "Data de validade não pode ser anterior a data atual"
            )
        return validade


class RequerenteForm(forms.Form):
    nome = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    telefone = forms.CharField(max_length=11, required=True)
    alimento = forms.CharField(max_length=100, required=True)

    # metodo validacao
    def clean_nome(self):
        nome = self.cleaned_data["nome"]
        if nome.isnumeric():
            raise forms.ValidationError("Nome não pode ser numerico")
        return nome

    # telefone do requerente deve conter 11 numeros
    def clean_telefone(self):
        telefone = self.cleaned_data["telefone"]
        if len(telefone) != 11:
            raise forms.ValidationError("Telefone deve conter 11 numeros")
        return telefone

    # email deve conter @
    def clean_email(self):
        email = self.cleaned_data["email"]
        if "@" not in email:
            raise forms.ValidationError("Email deve conter @")
        return email

    # nao deve conter numero e caracteres especiais
    def clean_alimento(self):
        alimento = self.cleaned_data["alimento"]
        if alimento.isnumeric():
            raise forms.ValidationError("Alimento não pode ser numerico")
        return alimento
