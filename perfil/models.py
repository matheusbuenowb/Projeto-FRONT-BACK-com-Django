from django.db import models
from datetime import datetime

class Categoria(models.Model):
    categoria = models.CharField(max_length=50)
    essencial = models.BooleanField(default = False)
    valor_planejamento = models.FloatField(default = 0)

    def __str__(self):
        return self.categoria
    
    def total_gasto(self):
        #se não fica o import circular infinito, um pouco complexo
        from extrato.models import Valores
        valores = Valores.objects.filter(categoria__id = self.id).filter(data__month = datetime.now().month).filter(tipo = 'S')
        total_valor = 0

        #TO DO: fazer uma função específico desse for
        for valor in valores:
            total_valor += valor.valor 
        return total_valor
    
    def calcula_percentual_gasto_por_categoria(self):
        #print(f"Total gasto: {self.total_gasto}")
        #print(f"Valor planejamento: {self.valor_planejamento}")
        if(self.valor_planejamento > 0):
            return int((self.total_gasto() * 100)/self.valor_planejamento)
        else:
            return 100
        #valor_planejamento  --> 100%
        #total_gasto -->          ?


class Conta(models.Model):
    banco_choices = (
        ('NU', 'Nubank'),
        ('CE', 'Caixa Econômica'),
        ('BR', 'Bradesco')
    )

    tipo_choices = (
        ('pf', 'Pessoa física'),
        ('pj', 'Pessoa Jurídica')
    )

    apelido = models.CharField(max_length=50)
    banco = models.CharField(max_length = 2, choices = banco_choices)
    tipo = models.CharField(max_length = 2, choices = tipo_choices)
    valor = models.FloatField()
    icone = models.ImageField(upload_to = "icones")

    def __str__(self):
        return self.apelido
    