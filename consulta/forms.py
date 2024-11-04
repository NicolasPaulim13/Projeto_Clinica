# forms.py do app consulta
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
        fields = ['assunto', 'data_consulta', 'hora_consulta', 'observacoes', 'medico']
