from django.urls import path
from . import views

urlpatterns = [
    path('', views.cadastro_registro, name='cadastro_registro'),
    path('create/', views.cadastro_create_paciente, name='cadastro_create_paciente'),
]


