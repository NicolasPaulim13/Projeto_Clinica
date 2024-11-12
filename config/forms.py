# forms.py
from django import forms
from .models import Perfil
from cadastro_registro.models import CadastroRegistro

class PerfilForm(forms.ModelForm):
    nome_paciente = forms.CharField(max_length=100, required=True, label="Nome")
    email_paciente = forms.EmailField(required=True, label="Email")
    cpf_paciente = forms.CharField(max_length=11, required=True, label="CPF")
    data_nascimento_paciente = forms.DateField(required=True, label="Data de Nascimento")
    senha_paciente = forms.CharField(widget=forms.PasswordInput(), required=True, label="Senha")

    class Meta:
        model = Perfil
        fields = ['imagem_perfil']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.cadastro_registro:
            cadastro = self.instance.cadastro_registro
            self.fields['nome_paciente'].initial = cadastro.nome_paciente
            self.fields['email_paciente'].initial = cadastro.email_paciente
            self.fields['cpf_paciente'].initial = cadastro.cpf_paciente
            self.fields['data_nascimento_paciente'].initial = cadastro.data_nascimento_paciente
            self.fields['senha_paciente'].initial = cadastro.senha_paciente

    def save(self, commit=True):
        perfil = super().save(commit=False)
        cadastro = perfil.cadastro_registro
        cadastro.nome_paciente = self.cleaned_data['nome_paciente']
        cadastro.email_paciente = self.cleaned_data['email_paciente']
        cadastro.cpf_paciente = self.cleaned_data['cpf_paciente']
        cadastro.data_nascimento_paciente = self.cleaned_data['data_nascimento_paciente']
        cadastro.senha_paciente = self.cleaned_data['senha_paciente']
        cadastro.save()
        if commit:
            perfil.save()
        return perfil
