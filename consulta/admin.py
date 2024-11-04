from django.contrib import admin
from .models import Consulta  # Importando o modelo Consulta

# Registrando o modelo Consulta no admin
@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone', 'assunto', 'data_consulta', 'hora_consulta', 'observacoes')  # Campos a serem exibidos na lista de admin
    search_fields = ('nome', 'email', 'telefone', 'assunto')  # Campos disponíveis para busca

# Se você tiver outros modelos, registre-os aqui também
