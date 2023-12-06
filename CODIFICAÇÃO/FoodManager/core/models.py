from django.db import models

# Create your models here.
from mongoengine import Document, fields


class Produto(Document):
    nome = fields.StringField(max_length=100)
    quantidade = fields.IntField()
    validade = fields.DateTimeField()
