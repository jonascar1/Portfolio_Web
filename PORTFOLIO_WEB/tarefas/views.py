

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Tarefa
from .serializers import TarefaSerializer

from rest_framework import generics




#! ok então esse estilo é bem mais direto, ele vai utilizar as generic views do próprio Django Rest para fazer toda a parte das requisições

# ─── Generic Views com autenticacao (VERSAO FINAL) ───

class TarefaListCreate(generics.ListCreateAPIView): # <-- No parâmetro é onde deve ser informado as generic view que vai ser utilizada
                                                                #como dito no arquivo md, isso é feito pelos "mixin"

    serializer_class = TarefaSerializer # como traduzir para JSON
    permission_classes = [IsAuthenticated]

    def get_queryset(self): #Queryset é basicamente para consultar 
                            # request.user contem o usuario autenticado pelo JWT.
        return Tarefa.objects.filter(responsavel=self.request.user) # Lembro de ser recomendado usar filter ao invés de get

    def perform_create(self, serializer):
        serializer.save(responsavel=self.request.user)


class TarefaDetail(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = TarefaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return Tarefa.objects.filter(responsavel=self.request.user)
    
    
    
    
    
    
'''' Estilos Não utilizados - Ignorar, decidi deixar apenas para visualizar as maneiras possíveis de ser feito:

# ─── Estilo 1: Function-Based Views (@api_view) ───   
    É feito um método no qual todas as requisições https precisam ser manuais


@api_view(['GET', 'POST'])  # <-- Quais requisições https serão utilizadas no método
def tarefa_list_create_fbv(request):

    if request.method == 'GET':
        tarefas = Tarefa.objects.all()
        serializer = TarefaSerializer(tarefas, many=True)
        # Response() = substitui o render() do Django
        # Em vez de HTML, retorna JSON automaticamente!
        return Response(serializer.data)             # ---> JSON com lista de tarefas

    elif request.method == 'POST':
        # request.data = corpo JSON enviado pelo cliente (substitui request.POST)
        serializer = TarefaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)   # ---> 201 Código de ação bem sucedida
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # ---> 400 código para dizer que houve problema relacionado ao dados estarem incorretos


@api_view(['GET', 'PUT', 'DELETE'])

def tarefa_detail_fbv(request, pk): # <-- Método que é responsável pela execução dos requisições
                                    #Com os devidos tratamentos de erros e tals
    try:
        tarefa = Tarefa.objects.get(pk=pk) 
    except Tarefa.DoesNotExist:
        return Response(
            {'erro': 'Tarefa nao encontrada'},
            status=status.HTTP_404_NOT_FOUND      #erro de não encontrado
        )

    if request.method == 'GET':
        serializer = TarefaSerializer(tarefa) 
        return Response(serializer.data)         # <-- se der tudo certo, retorna o json com os dados

    elif request.method == 'PUT':               ## <-- Aqui seria a atualização total (PUT) dos dados, 
        serializer = TarefaSerializer(tarefa, data=request.data) 
        if serializer.is_valid(): 
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        tarefa.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 
        
from rest_framework.views import APIView


#! ─── Estilo 2: Class-Based Views (APIView) ───
    #Nesse outro as requisições são feito através de métodos de uma classe
    #percebi que em relação ao estilo 3, os estilos 1 e 2 são bastantes "grandes"/manuais


class TarefaListCreateAPIView(APIView):
    """
    GET  /api/tarefas/v2/ → Lista todas as tarefas
    POST /api/tarefas/v2/ → Cria uma nova tarefa
    """

    def get(self, request):                          # GET /api/tarefas/v2/
        tarefas = Tarefa.objects.all()
        serializer = TarefaSerializer(tarefas, many=True)
        return Response(serializer.data)             # ---> JSON lista

    def post(self, request):                         # POST /api/tarefas/v2/
        serializer = TarefaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# URL: path('v2/<int:pk>/', views.TarefaDetailAPIView.as_view())

class TarefaDetailAPIView(APIView):
    """
    GET    /api/tarefas/v2/<pk>/ → Retorna uma tarefa
    PUT    /api/tarefas/v2/<pk>/ → Atualiza uma tarefa
    DELETE /api/tarefas/v2/<pk>/ → Exclui uma tarefa
    """

    def get_object(self, pk):
        try:
            return Tarefa.objects.get(pk=pk)
        except Tarefa.DoesNotExist:
            return None

    def get(self, request, pk):                      # GET /api/tarefas/v2/1/
        tarefa = self.get_object(pk)
        if tarefa is None:
            return Response(
                {'erro': 'Tarefa nao encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = TarefaSerializer(tarefa)
        return Response(serializer.data)

    def put(self, request, pk):                      # PUT /api/tarefas/v2/1/
        tarefa = self.get_object(pk)
        if tarefa is None:
            return Response(
                {'erro': 'Tarefa nao encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = TarefaSerializer(tarefa, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):                   # DELETE /api/tarefas/v2/1/
        tarefa = self.get_object(pk)
        if tarefa is None:
            return Response(
                {'erro': 'Tarefa nao encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )
        tarefa.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)'''