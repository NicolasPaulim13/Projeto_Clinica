# Generated by Django 5.1.3 on 2024-11-20 19:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cadastro_registro", "0016_alter_cadastroregistro_user_delete_perfil"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="cadastroregistro",
            options={
                "verbose_name": "Cadastro de Paciente",
                "verbose_name_plural": "Cadastros de Pacientes",
            },
        ),
        migrations.AlterField(
            model_name="cadastroregistro",
            name="cpf_paciente",
            field=models.CharField(
                max_length=14, unique=True, verbose_name="CPF do Paciente"
            ),
        ),
        migrations.AlterField(
            model_name="cadastroregistro",
            name="data_nascimento_paciente",
            field=models.DateField(verbose_name="Data de Nascimento"),
        ),
        migrations.AlterField(
            model_name="cadastroregistro",
            name="email_paciente",
            field=models.EmailField(
                max_length=254, unique=True, verbose_name="Email do Paciente"
            ),
        ),
        migrations.AlterField(
            model_name="cadastroregistro",
            name="imagem_perfil",
            field=models.ImageField(
                blank=True,
                default="img/perfil-icon.png",
                null=True,
                upload_to="imagens_perfil/",
                verbose_name="Imagem de Perfil",
            ),
        ),
        migrations.AlterField(
            model_name="cadastroregistro",
            name="nome_paciente",
            field=models.CharField(max_length=100, verbose_name="Nome do Paciente"),
        ),
        migrations.AlterField(
            model_name="cadastroregistro",
            name="senha_paciente",
            field=models.CharField(max_length=255, verbose_name="Senha do Paciente"),
        ),
        migrations.AlterField(
            model_name="cadastroregistro",
            name="sexo_paciente",
            field=models.CharField(
                choices=[("M", "Masculino"), ("F", "Feminino"), ("O", "Outro")],
                max_length=1,
                verbose_name="Sexo",
            ),
        ),
        migrations.AlterField(
            model_name="cadastroregistro",
            name="tipo_usuario",
            field=models.CharField(
                default="paciente", max_length=50, verbose_name="Tipo de Usuário"
            ),
        ),
        migrations.AlterField(
            model_name="cadastroregistro",
            name="user",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="cadastro_paciente",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Usuário",
            ),
        ),
    ]
