from django.db import models
from django.conf import settings  # Importando settings para referenciar o modelo User

class CadastroRegistro(models.Model):
    nome_paciente = models.CharField(max_length=100)
    email_paciente = models.EmailField()
    cpf_paciente = models.CharField(max_length=11)
    data_nascimento_paciente = models.DateField()
    sexo_paciente = models.CharField(
        max_length=1, choices=[('M', 'Masculino'), ('F', 'Feminino'), ('O', 'Outro')]
    )
    senha_paciente = models.CharField(max_length=255)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True
    )
    imagem_perfil = models.ImageField(
        upload_to='imagens_perfil/', default='img/perfil-icon.png', null=True, blank=True
    )
    tipo_usuario = models.CharField(max_length=50, default='paciente')

    def __str__(self):
        return self.nome_paciente
