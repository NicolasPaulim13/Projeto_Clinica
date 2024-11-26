# Generated by Django 5.1.3 on 2024-11-26 04:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("consulta", "0010_consulta_avaliacao_cavidade_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="consulta",
            name="avaliacao_cavidade",
            field=models.TextField(
                blank=True,
                default="Não avaliada",
                null=True,
                verbose_name="Avaliação da Cavidade Bucal",
            ),
        ),
        migrations.AlterField(
            model_name="consulta",
            name="cirurgias_anteriores",
            field=models.TextField(
                blank=True,
                default="Sem cirurgias anteriores",
                null=True,
                verbose_name="Cirurgias Anteriores",
            ),
        ),
        migrations.AlterField(
            model_name="consulta",
            name="condicoes_saude",
            field=models.TextField(
                blank=True,
                default="Sem informações registradas",
                null=True,
                verbose_name="Condições de Saúde Geral",
            ),
        ),
        migrations.AlterField(
            model_name="consulta",
            name="diagnostico_detalhado",
            field=models.TextField(
                blank=True,
                default="Sem diagnóstico detalhado",
                null=True,
                verbose_name="Diagnóstico Detalhado",
            ),
        ),
        migrations.AlterField(
            model_name="consulta",
            name="documento_identificacao",
            field=models.CharField(
                blank=True,
                default="Documento não informado",
                max_length=50,
                null=True,
                verbose_name="Documento de Identificação",
            ),
        ),
        migrations.AlterField(
            model_name="consulta",
            name="endereco_contato",
            field=models.CharField(
                blank=True,
                default="Endereço não informado",
                max_length=255,
                null=True,
                verbose_name="Endereço e Contato",
            ),
        ),
        migrations.AlterField(
            model_name="consulta",
            name="historico_tratamentos",
            field=models.TextField(
                blank=True,
                default="Sem histórico registrado",
                null=True,
                verbose_name="Histórico de Tratamentos Odontológicos",
            ),
        ),
        migrations.AlterField(
            model_name="consulta",
            name="lesoes_anomalias",
            field=models.TextField(
                blank=True,
                default="Nenhuma lesão identificada",
                null=True,
                verbose_name="Presença de Lesões ou Anomalias",
            ),
        ),
        migrations.AlterField(
            model_name="consulta",
            name="procedimentos_planejados",
            field=models.TextField(
                blank=True,
                default="Nenhum procedimento planejado",
                null=True,
                verbose_name="Procedimentos Planejados",
            ),
        ),
        migrations.AlterField(
            model_name="consulta",
            name="queixas_principais",
            field=models.TextField(
                blank=True,
                default="Nenhuma queixa registrada",
                null=True,
                verbose_name="Queixas Principais do Paciente",
            ),
        ),
    ]
