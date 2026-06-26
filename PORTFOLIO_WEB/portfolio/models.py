
# Create your models here.
from django.db import models
class Projeto(models.Model):
    
    def __str__(self):
        return self.name
    
    type_project = models.CharField(max_length=30)
    name = models.CharField(max_length=60)
    description = models.TextField(max_length=700)
    github_link = models.URLField(max_length=200)
    
    
class Certificado(models.Model):
    def __str__(self):
        return self.description

    description = models.TextField(max_length=700)
    