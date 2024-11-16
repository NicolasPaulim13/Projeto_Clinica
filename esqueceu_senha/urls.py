from django.urls import path
from .views import esqueceu_senha_view, codigo_senha_view, redefinir_senha_view # Certifique-se de importar as views

urlpatterns = [
    path('esqueceu_senha/', esqueceu_senha_view, name='esqueceu_senha'),
    path('codigo_senha/', codigo_senha_view, name='codigo_senha'),
    path('redefinir_senha/', redefinir_senha_view, name='redefinir_senha'),
]
