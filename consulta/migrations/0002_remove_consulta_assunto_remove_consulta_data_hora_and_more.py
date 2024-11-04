# Generated by Django 5.1.2 on 2024-10-28 14:23

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cadastro_registro", "0006_alter_cadastroregistro_user"),
        ("consulta", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="consulta",
            name="assunto",
        ),
        migrations.RemoveField(
            model_name="consulta",
            name="data_hora",
        ),
        migrations.RemoveField(
            model_name="consulta",
            name="email",
        ),
        migrations.RemoveField(
            model_name="consulta",
            name="nome",
        ),
        migrations.RemoveField(
            model_name="consulta",
            name="observacoes",
        ),
        migrations.RemoveField(
            model_name="consulta",
            name="telefone",
        ),
        migrations.AddField(
            model_name="consulta",
            name="data_consulta",
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name="consulta",
            name="hora_consulta",
            field=models.TimeField(default=datetime.time(8, 0)),
        ),
        migrations.AddField(
            model_name="consulta",
            name="paciente",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="cadastro_registro.cadastroregistro",
            ),
        ),
    ]