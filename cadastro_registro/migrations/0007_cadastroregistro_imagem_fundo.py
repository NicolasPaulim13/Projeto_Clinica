# Generated by Django 5.1.2 on 2024-10-28 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cadastro_registro", "0006_alter_cadastroregistro_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="cadastroregistro",
            name="imagem_fundo",
            field=models.ImageField(blank=True, null=True, upload_to="imagens_fundo/"),
        ),
    ]
