# models.py do app consulta
from django.db import models
from cadastro_registro.models import CadastroRegistro
from django.conf import settings
from datetime import time, date

class Consulta(models.Model):
    # Campos existentes
    ASSUNTO_OPCOES = [
        ('avaliacao_diagnostico', 'Avaliação e Diagnóstico'),
        ('tratamentos_restauradores', 'Tratamentos Restauradores'),
        ('tratamentos_periodontais', 'Tratamentos Periodontais'),
        ('odontopediatria', 'Odontopediatria'),
        ('ortodontia', 'Ortodontia'),
        ('odontologia_estetica', 'Odontologia Estética'),
        ('cirurgia_oral', 'Cirurgia Oral'),
        ('proteses_dentarias', 'Próteses Dentárias'),
        ('consultas_emergencia', 'Consultas de Emergência'),
        ('acompanhamento_manutencao', 'Acompanhamento e Manutenção'),
    ]

    paciente = models.ForeignKey(CadastroRegistro, on_delete=models.CASCADE, null=True)
    nome = models.CharField(max_length=100, default="Nome Desconhecido")
    email = models.EmailField()
    telefone = models.CharField(max_length=20, default="0000-0000")
    assunto = models.CharField(max_length=50, choices=ASSUNTO_OPCOES, default='avaliacao_diagnostico')
    data_consulta = models.DateField(default=date.today)
    hora_consulta = models.TimeField(default=time(8, 0))
    observacoes = models.TextField(blank=True, null=True)
    medico = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'groups__name': 'medico'})

    def __str__(self):
        return f'Consulta de {self.nome} em {self.data_consulta} às {self.hora_consulta}'
