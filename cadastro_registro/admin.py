from django.contrib import admin
from .models import CadastroRegistro

@admin.register(CadastroRegistro)
class CadastroRegistroAdmin(admin.ModelAdmin):
    list_display = (
        'nome_paciente', 
        'email_paciente', 
        'cpf_paciente', 
        'data_nascimento_paciente', 
        'sexo_paciente',
        'user'
    )
    search_fields = ('nome_paciente', 'email_paciente', 'cpf_paciente', 'user__username')

