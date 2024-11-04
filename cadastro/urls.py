from django.urls import path
from .views import login_page  # Importa a nova view de login

urlpatterns = [
    path('login/', login_page, name='login'),  # Rota para a página de login
]
