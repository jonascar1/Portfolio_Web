from django.urls import include, path
from config import settings
from . import views
from django.conf.urls.static import static

app_name = 'portfolio'

urlpatterns = [
    path('', views.home, name='home'),
    path('projetos/', views.projetos, name='projetos'),
] 