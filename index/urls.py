from django.urls import path
from .views import index, logout_view
from . import views

# Lista de padrões de URL para a aplicação 'index'
urlpatterns = [
    path('', index, name='index'),
    path('logout/', logout_view, name='logout'),  # Rota para o logout
    path('edit-profile/', views.edit_profile, name='edit_profile'),
]
