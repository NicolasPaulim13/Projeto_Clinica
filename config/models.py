# models.py
from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100, blank=True)
    imagem_perfil = models.ImageField(upload_to='perfil_imagens/', blank=True, null=True)
    acessibilidade = models.JSONField(default=dict)  # Exemplo: {"font_size": "medium", "contrast": "normal"}

    def __str__(self):
        return self.user.username
