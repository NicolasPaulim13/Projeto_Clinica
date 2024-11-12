# config/models.py

from django.db import models
from django.contrib.auth.models import User
from cadastro_registro.models import CadastroRegistro

class Perfil(models.Model):
    config_user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)  # Adicione null=True e blank=True temporariamente
    cadastro_registro = models.OneToOneField(CadastroRegistro, on_delete=models.CASCADE)
    imagem_perfil = models.ImageField(upload_to='perfil_imagens/', blank=True, null=True)
    acessibilidade = models.JSONField(default=dict)

    def __str__(self):
        return self.cadastro_registro.nome_paciente if self.cadastro_registro else "Perfil sem CadastroRegistro"
