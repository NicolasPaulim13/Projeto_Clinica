# Generated by Django 5.1.3 on 2024-11-12 13:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cadastro_registro", "0012_alter_cadastroregistro_tipo_usuario"),
        ("config", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="perfil",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                to="cadastro_registro.cadastroregistro",
            ),
        ),
    ]
