from django import forms
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from validate_docbr import CPF
from .models import CadastroRegistro
import re

class CadastroRegistroForm(forms.ModelForm):
    confirma_senha_paciente = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirme sua senha'}),
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
            'data_nascimento_paciente': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_cpf_paciente(self):
        cpf = self.cleaned_data.get('cpf_paciente')

        # Remover pontuações e espaços antes de validar
        cpf = re.sub(r'\D', '', cpf)

        if len(cpf) != 11:
            raise ValidationError("CPF deve ter 11 dígitos.")
    
        # Validar o CPF com a biblioteca `validate-docbr`
        cpf_validator = CPF()
        if not cpf_validator.validate(cpf):
            raise ValidationError("CPF inválido. Verifique e tente novamente.")

        return cpf

    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get("senha_paciente")
        confirma_senha = cleaned_data.get("confirma_senha_paciente")

        # Debugging para verificar valores
        print(f"Senha: {senha}, Confirmação: {confirma_senha}")

        if senha and confirma_senha and senha != confirma_senha:
            self.add_error('confirma_senha_paciente', "As senhas não coincidem. Tente novamente.")
            raise ValidationError("As senhas não coincidem. Tente novamente.")
    
        return cleaned_data


    def save(self, commit=True):
        instance = super(CadastroRegistroForm, self).save(commit=False)
        instance.senha_paciente = make_password(self.cleaned_data['senha_paciente'])
        if commit:
            instance.save()
        return instance
