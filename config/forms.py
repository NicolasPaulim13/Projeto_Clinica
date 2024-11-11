# forms.py
from django import forms
from cadastro_registro.models import CadastroRegistro

# forms.py
# forms.py
from django import forms
from cadastro_registro.models import CadastroRegistro

class PerfilForm(forms.ModelForm):
    class Meta:
        model = CadastroRegistro
        fields = ['nome_paciente']  # Campo apenas para o nome

    
    def save(self, commit=True):
        instance = super().save(commit=False)
        # Atualiza a senha do user associado
        if instance.senha_paciente:
            instance.user.set_password(instance.senha_paciente)
        if commit:
            instance.save()
            instance.user.save()  # Salva o objeto user também
        return instance
