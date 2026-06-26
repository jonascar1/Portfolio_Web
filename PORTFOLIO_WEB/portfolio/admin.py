from django.contrib import admin

from portfolio.models import Certificado, Projeto

# Register your models here.
admin.site.register(Projeto)
admin.site.register(Certificado)