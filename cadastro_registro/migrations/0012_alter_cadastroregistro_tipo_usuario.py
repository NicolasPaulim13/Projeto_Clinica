# Generated by Django 5.1.1 on 2024-11-04 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cadastro_registro", "0011_alter_cadastroregistro_tipo_usuario"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cadastroregistro",
            name="tipo_usuario",
            field=models.CharField(default="paciente", max_length=50),
        ),
    ]
