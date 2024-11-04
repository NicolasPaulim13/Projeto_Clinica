# cadastro_adm/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_medico, name='login_medico'),
]
