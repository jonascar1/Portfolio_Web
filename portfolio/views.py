from django.shortcuts import render


def home(request):
    return render(request, 'portfolio/home.html')


def projetos(request):
    return render(request, 'portfolio/projetos.html')