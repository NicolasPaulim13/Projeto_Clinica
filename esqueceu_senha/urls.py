from django.urls import path
from .views import esqueceu_senha_view  # Importa a função de view correta

# Lista de padrões de URL para a aplicação 'esqueceu_senha'
urlpatterns = [
    path('', esqueceu_senha_view, name='esqueceu_senha'),  # Usa o nome correto da função
    path('esqueceu_senha/', esqueceu_senha_view, name='esqueceu_senha'),  # Redundante, mas pode manter se desejar
]
