# Generated by Django 5.1.1 on 2024-09-17 12:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cadastro_registro', '0002_cadastroregistro_delete_patient'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cadastroregistro',
            old_name='confirma_senha',
            new_name='confirma_senha_paciente',
        ),
        migrations.RenameField(
            model_name='cadastroregistro',
            old_name='cpf',
            new_name='cpf_paciente',
        ),
        migrations.RenameField(
            model_name='cadastroregistro',
            old_name='data_nascimento',
            new_name='data_nascimento_paciente',
        ),
        migrations.RenameField(
            model_name='cadastroregistro',
            old_name='email',
            new_name='email_paciente',
        ),
        migrations.RenameField(
            model_name='cadastroregistro',
            old_name='nome_usuario',
            new_name='nome_paciente',
        ),
        migrations.RenameField(
            model_name='cadastroregistro',
            old_name='senha',
            new_name='senha_paciente',
        ),
        migrations.RenameField(
            model_name='cadastroregistro',
            old_name='sexo',
            new_name='sexo_paciente',
        ),
    ]
