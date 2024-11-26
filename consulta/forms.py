from django import forms
from .models import Consulta
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

class ConsultaForm(forms.ModelForm):
    medico = forms.ModelChoiceField(
        queryset=User.objects.filter(groups__name='medico'),
        required=False,
        label="Escolha o médico"
    )

    class Meta:
        model = Consulta
        fields = ['telefone', 'medico', 'assunto', 'data_consulta', 'hora_consulta', 'observacoes']

class ProntuarioCompletoForm(forms.ModelForm):
    def clean_documento_identificacao(self):
        documento = self.cleaned_data.get('documento_identificacao')
        if not re.match(r'^\d{2}\.\d{3}\.\d{3}-\d{2}$', documento):
            raise ValidationError('O documento de identificação não está no formato correto (XX.XXX.XXX-XX).')
        return documento

    class Meta:
        model = Consulta
        fields = [
            'nome_paciente', 'data_nascimento', 'genero', 'endereco_contato',
            'documento_identificacao', 'condicoes_saude', 'cirurgias_anteriores',
            'historico_tratamentos', 'avaliacao_cavidade', 'lesoes_anomalias',
            'queixas_principais', 'diagnostico_detalhado', 'procedimentos_planejados',
        ]

