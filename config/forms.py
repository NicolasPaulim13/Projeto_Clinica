from django import forms
from .models import Perfil
from cadastro_registro.models import CadastroRegistro
from django.contrib.auth.hashers import make_password

class PerfilForm(forms.ModelForm):
    nome_paciente = forms.CharField(max_length=100, required=True, label="Nome")
    email_paciente = forms.EmailField(required=True, label="Email")
    cpf_paciente = forms.CharField(max_length=11, required=True, label="CPF")
    data_nascimento_paciente = forms.DateField(
        required=True, label="Data de Nascimento",
        widget=forms.DateInput(attrs={'type': 'date'})
    )
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

        # Atualizar os campos do CadastroRegistro
        if perfil.cadastro_registro:
            cadastro = perfil.cadastro_registro
            cadastro.nome_paciente = self.cleaned_data.get('nome_paciente', cadastro.nome_paciente)
            cadastro.email_paciente = self.cleaned_data.get('email_paciente', cadastro.email_paciente)
            cadastro.cpf_paciente = self.cleaned_data.get('cpf_paciente', cadastro.cpf_paciente)

            if not cadastro.cpf_paciente:
                raise ValueError("O CPF não pode ser vazio.")

            cadastro.data_nascimento_paciente = self.cleaned_data.get(
                'data_nascimento_paciente', cadastro.data_nascimento_paciente
            )

            # Hash da senha (caso ela seja alterada)
            senha_paciente = self.cleaned_data.get('senha_paciente')
            if senha_paciente and senha_paciente != cadastro.senha_paciente:
                cadastro.senha_paciente = make_password(senha_paciente)

            cadastro.save()

        if commit:
            perfil.save()
        return perfil
