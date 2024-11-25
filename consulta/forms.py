from django import forms
from .models import Consulta
from django.contrib.auth.models import User

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
    class Meta:
        model = Consulta
        fields = [
            'nome_paciente', 'data_nascimento', 'genero', 'endereco_contato', 
            'documento_identificacao', 'condicoes_saude', 'cirurgias_anteriores',
            'historico_tratamentos', 'avaliacao_cavidade', 'lesoes_anomalias',
            'queixas_principais', 'diagnostico_detalhado', 'procedimentos_planejados',
        ]
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
        }
