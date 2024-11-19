# consulta/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.agendar_consulta, name='consulta'),
    path('lista/', views.listar_consultas, name='consulta_list'),
    path('editar/<int:id>/', views.editar_consulta, name='consulta_edit'),
    path('<int:id>/deletar/', views.deletar_consulta, name='consulta_delete'),
    path('relatorio/', views.relatorio, name='relatorio'),
    path('prontuario/', views.prontuario, name='prontuario'),
]
