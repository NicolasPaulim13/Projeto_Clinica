from django.db import models
from django.contrib.auth.models import User
from cadastro_registro.models import CadastroRegistro


class Perfil(models.Model):
    config_user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        unique=True,  # Garante que cada usuário tenha apenas um perfil
        related_name='config_usuario',
        verbose_name="Usuário"
    )
    cadastro_registro = models.OneToOneField(
        CadastroRegistro,
        on_delete=models.CASCADE,
        related_name='perfil_config',
        verbose_name="Cadastro Registro"
    )
    imagem_perfil = models.ImageField(
        upload_to='perfil_imagens/',
        blank=True,
        null=True,
        default='img/perfil-icon.png',
        verbose_name="Imagem de Perfil"
    )
    acessibilidade = models.JSONField(default=dict, verbose_name="Configurações de Acessibilidade")

    class Meta:
        verbose_name = "Perfil de Configuração"
        verbose_name_plural = "Perfis de Configuração"

    def __str__(self):
        return self.cadastro_registro.nome_paciente if self.cadastro_registro else "Perfil sem CadastroRegistro"
