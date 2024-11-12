from django.urls import path
from . import views

urlpatterns = [
    path('config/', views.config, name='config'),  # Certifique-se de que o nome está correto

]
