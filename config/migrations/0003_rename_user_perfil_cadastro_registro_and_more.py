# Generated by Django 5.1.3 on 2024-11-12 14:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("config", "0002_alter_perfil_user"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name="perfil",
            old_name="user",
            new_name="cadastro_registro",
        ),
        migrations.RemoveField(
            model_name="perfil",
            name="nome",
        ),
        migrations.AddField(
            model_name="perfil",
            name="config_user",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
