from django import forms
from cadastro_registro.models import CadastroRegistro
from .models import Perfil

class PerfilForm(forms.ModelForm):
    # Campos vinculados ao CadastroRegistro
    nome_paciente = forms.CharField(
        max_length=100,
        label="Nome Completo",
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Digite seu nome completo'})
    )
    email_paciente = forms.EmailField(
        label="Email",
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'exemplo@email.com'})
    )
    cpf_paciente = forms.CharField(
        max_length=14,
        label="CPF",
        required=True,
        widget=forms.TextInput(attrs={'placeholder': '000.000.000-00'})
    )
    data_nascimento_paciente = forms.DateField(
        label="Data de Nascimento",
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Perfil
        fields = ['imagem_perfil']  # Campo relacionado ao Perfil

    def save(self, commit=True, cadastro=None):
        """
        Sobrescreve o método save para atualizar também os campos do CadastroRegistro.
        """
        perfil = super().save(commit=False)

        if cadastro:
            cadastro.nome_paciente = self.cleaned_data.get('nome_paciente')
            cadastro.email_paciente = self.cleaned_data.get('email_paciente')
            cadastro.cpf_paciente = self.cleaned_data.get('cpf_paciente')
            cadastro.data_nascimento_paciente = self.cleaned_data.get('data_nascimento_paciente')
            if commit:
                cadastro.save()

        if commit:
            perfil.save()

        return perfil
