from django.db import models
from django.conf import settings 


class Tarefa(models.Model):
    
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    concluida = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)

    # null=True e blank=True para nao quebrar tarefas ja existentes
    responsavel = models.ForeignKey(
        settings.AUTH_USER_MODEL,       
        on_delete=models.CASCADE,      
        related_name='tarefas',         # Permite acessar: user.tarefas.all()
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ['-criado_em']

    def __str__(self):
        return self.titulo
 
 # ok deu pra entender tudo aqui. Apenas uma classe simples, única coisa nova é a classe Meta, para fazer registro de criação.