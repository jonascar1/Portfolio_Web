from django.shortcuts import render
from core.models import BancoPessoal
from portfolio.models import Certificado, Projeto


def home(request):
    profile = BancoPessoal.objects.all().first()
    
    certificado = Certificado.objects.all()
    
    return render(request, 'portfolio/home.html', {"profile": profile, "certificado": certificado})


def projetos(request):
    projeto = Projeto.objects.all().first()
    
    return render(request, 'portfolio/projetos.html', {"projeto": projeto})

def contato(request):
    return render(request,'portfolio/projetos.html')