from django.db import models
class BancoPessoal(models.Model):
    
    def __str__(self):
        return self.name
    
    profile_image = models.ImageField(upload_to = 'profiles/', blank =True)
    # Eu ia deixar o ImageField com o "default=" pra que já encontrasse, mas como você vai poder alterar pelo admin (foi isso que entendi)
    # Eu preferi deixar sem o default
    name = models.CharField(max_length=60)
    description = models.TextField(max_length=700)
    course = models.CharField(max_length= 70)
    period = models.CharField(max_length=12)
    email = models.EmailField(max_length=100)
    github = models.URLField(max_length=200)
    linkedin = models.URLField(max_length=200)


from django.db import models
from django.conf import settings


class Pessoal(models.Model):
    # Vincula o perfil a um usuario do Django
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='perfil',
        null=True,
        blank=True,
    )

    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    curso = models.CharField(max_length=200)
    periodo = models.CharField(max_length=50)
    email = models.EmailField()
    git = models.URLField(blank=True)
    linked = models.URLField(blank=True)
    url_imagem = models.URLField(blank=True)

    class Meta:
        verbose_name = 'Perfil Pessoal'
        verbose_name_plural = 'Perfis Pessoais'

    def __str__(self):
        return self.nome