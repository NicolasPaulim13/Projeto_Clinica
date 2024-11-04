from django import forms
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from .models import CadastroRegistro

class CadastroRegistroForm(forms.ModelForm):
    confirma_senha_paciente = forms.CharField(
        widget=forms.PasswordInput, 
        label='Confirme sua Senha'
    )
    
    class Meta:
        model = CadastroRegistro
        fields = [
            'nome_paciente', 
            'email_paciente', 
            'cpf_paciente', 
            'data_nascimento_paciente', 
            'sexo_paciente', 
            'senha_paciente'
        ]
        widgets = {
            'senha_paciente': forms.PasswordInput(attrs={'placeholder': 'Senha'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get("senha_paciente")
        confirma_senha = cleaned_data.get("confirma_senha_paciente")
        
        if senha and confirma_senha and senha != confirma_senha:
            raise ValidationError("As senhas não coincidem. Tente novamente.")
        
        return cleaned_data

    def save(self, commit=True):
        instance = super(CadastroRegistroForm, self).save(commit=False)
        instance.senha_paciente = make_password(self.cleaned_data['senha_paciente'])
        if commit:
            instance.save()
        return instance

