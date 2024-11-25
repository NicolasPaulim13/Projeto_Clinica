from django.contrib import admin
from .models import Consulta

@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone', 'assunto', 'data_consulta', 'hora_consulta', 'observacoes', 'exame_realizado')
    list_filter = ('data_consulta', 'assunto', 'exame_realizado')
    search_fields = ('nome', 'email', 'telefone', 'assunto')
    readonly_fields = ('nome', 'email', 'telefone')
    list_per_page = 20
    actions = ['marcar_exame_realizado']

    def marcar_exame_realizado(self, request, queryset):
        queryset.update(exame_realizado=True)
        self.message_user(request, "Consultas marcadas como realizadas com sucesso.")
    marcar_exame_realizado.short_description = "Marcar exames como realizados"
