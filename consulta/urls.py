# consulta/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.agendar_consulta, name='consulta'),
    path('lista/', views.consulta_list, name='consulta_list'),
    path('editar/<int:id>/', views.editar_consulta, name='consulta_edit'),
    path('<int:id>/deletar/', views.deletar_consulta, name='consulta_delete'),
    path('relatorio/', views.relatorio, name='relatorio'),
    path('consulta/prontuario/<int:id>/', views.prontuario, name='prontuario'),
    path('prontuario/<int:id>/editar/', views.editar_prontuario_completo, name='editar_prontuario_completo'),
    path('consultas_realizadas/<int:medico_id>/', views.consultas_realizadas, name='consultas_realizadas'),
    path('finalizar_consulta/<int:pk>/', views.finalizar_consulta, name='finalizar_consulta'),
]
