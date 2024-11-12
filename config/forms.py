# forms.py
from django import forms
from .models import Perfil  # Importa o modelo Perfil

class PerfilForm(forms.ModelForm):
    nome_paciente = forms.CharField(
        max_length=100,
        required=True,
        label="Nome",
        help_text="Edite o nome do paciente"
    )

    class Meta:
        model = Perfil
        fields = ['imagem_perfil']  # Inclui apenas imagem_perfil para edição de imagem no Perfil

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Inicializa o campo 'nome_paciente' com o nome do cadastro_registro relacionado
        if self.instance and self.instance.cadastro_registro:
            self.fields['nome_paciente'].initial = self.instance.cadastro_registro.nome_paciente

    def save(self, commit=True):
        perfil = super().save(commit=False)
        # Atualiza o nome do CadastroRegistro associado
        nome_paciente = self.cleaned_data.get('nome_paciente')
        if perfil.cadastro_registro and nome_paciente:
            perfil.cadastro_registro.nome_paciente = nome_paciente
            perfil.cadastro_registro.save()
        if commit:
            perfil.save()
        return perfil
