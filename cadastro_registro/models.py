from django.db import models
from django.conf import settings  # Para referenciar o AUTH_USER_MODEL


class CadastroRegistro(models.Model):
    nome_paciente = models.CharField(max_length=100, verbose_name="Nome do Paciente")
    email_paciente = models.EmailField(unique=True, verbose_name="Email do Paciente")
    cpf_paciente = models.CharField(max_length=14, unique=True, verbose_name="CPF do Paciente")
    data_nascimento_paciente = models.DateField(verbose_name="Data de Nascimento")
    sexo_paciente = models.CharField(
        max_length=1,
        choices=[('M', 'Masculino'), ('F', 'Feminino'), ('O', 'Outro')],
        verbose_name="Sexo"
    )
    senha_paciente = models.CharField(max_length=255, verbose_name="Senha do Paciente")
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        unique=True,  # Cada usuário deve estar associado a apenas um CadastroRegistro
        related_name='cadastro_paciente',
        verbose_name="Usuário"
    )
    imagem_perfil = models.ImageField(
        upload_to='imagens_perfil/',
        default='img/perfil-icon.png',
        null=True,
        blank=True,
        verbose_name="Imagem de Perfil"
    )
    tipo_usuario = models.CharField(max_length=50, default='paciente', verbose_name="Tipo de Usuário")

    class Meta:
        verbose_name = "Cadastro de Paciente"
        verbose_name_plural = "Cadastros de Pacientes"

    def __str__(self):
        return self.nome_paciente
