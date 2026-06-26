from django.contrib import admin
from .models import Tarefa


@admin.register(Tarefa)
class TarefaAdmin(admin.ModelAdmin):

    list_display = ['titulo', 'concluida', 'criado_em']
    list_filter = ['concluida']
    search_fields = ['titulo', 'descricao']
    
    # Isso é relativo a forma que é apresentada as tarefas na pag adm. A ordem, o filtro e os campos de pesquisa...