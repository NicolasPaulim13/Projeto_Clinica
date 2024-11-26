from django.db import models
from cadastro_registro.models import CadastroRegistro
from django.conf import settings
from datetime import time, date

class Consulta(models.Model):
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

    paciente = models.ForeignKey(
        CadastroRegistro,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    nome = models.CharField(
        max_length=100,
        default="Nome Desconhecido"
    )
    email = models.EmailField()
    telefone = models.CharField(
        max_length=20,
        default="0000-0000"
    )
    assunto = models.CharField(
        max_length=50,
        choices=ASSUNTO_OPCOES,
        default='avaliacao_diagnostico'
    )
    data_consulta = models.DateField(
        default=date.today
    )
    hora_consulta = models.TimeField(
        default=time(8, 0)
    )
    observacoes = models.TextField(
        blank=True,
        null=True
    )
    medico = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'groups__name': 'medico'}
    )
    nome_paciente = models.CharField(
        max_length=255,
        verbose_name="Nome Completo do Paciente",
        default="Nome Desconhecido"
    )
    data_nascimento = models.DateField(
        null=True,
        blank=True,
        verbose_name="Data de Nascimento"
    )
    genero = models.CharField(
        max_length=20,
        choices=[
            ('masculino', 'Masculino'),
            ('feminino', 'Feminino'),
            ('outro', 'Outro')
        ],
        verbose_name="Gênero",
        default='masculino'
    )
    endereco_contato = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Endereço e Contato",
        default="Endereço não informado"
    )
    documento_identificacao = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Documento de Identificação",
        default="Documento não informado"
    )
    condicoes_saude = models.TextField(
        null=True,
        blank=True,
        verbose_name="Condições de Saúde Geral",
        default="Sem informações registradas"
    )
    cirurgias_anteriores = models.TextField(
        null=True,
        blank=True,
        verbose_name="Cirurgias Anteriores",
        default="Sem cirurgias anteriores"
    )
    historico_tratamentos = models.TextField(
        null=True,
        blank=True,
        verbose_name="Histórico de Tratamentos Odontológicos",
        default="Sem histórico registrado"
    )
    avaliacao_cavidade = models.TextField(
        null=True,
        blank=True,
        verbose_name="Avaliação da Cavidade Bucal",
        default="Não avaliada"
    )
    lesoes_anomalias = models.TextField(
        null=True,
        blank=True,
        verbose_name="Presença de Lesões ou Anomalias",
        default="Nenhuma lesão identificada"
    )
    queixas_principais = models.TextField(
        null=True,
        blank=True,
        verbose_name="Queixas Principais do Paciente",
        default="Nenhuma queixa registrada"
    )
    diagnostico_detalhado = models.TextField(
        null=True,
        blank=True,
        verbose_name="Diagnóstico Detalhado",
        default="Sem diagnóstico detalhado"
    )
    procedimentos_planejados = models.TextField(
        null=True,
        blank=True,
        verbose_name="Procedimentos Planejados",
        default="Nenhum procedimento planejado"
    )
    exame_realizado = models.BooleanField(
        default=False,
        verbose_name="Exame Realizado"
    )

    def __str__(self):
        return f'Consulta de {self.nome} em {self.data_consulta} às {self.hora_consulta}'
