from djongo import models

class Modelo(models.Model):
    campo1 = models.CharField(max_length=100)
    campo2 = models.IntegerField()

    def __str__(self) -> str:
        return self.campo1