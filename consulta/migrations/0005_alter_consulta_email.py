# Generated by Django 5.1.2 on 2024-10-28 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("consulta", "0004_remove_consulta_paciente"),
    ]

    operations = [
        migrations.AlterField(
            model_name="consulta",
            name="email",
            field=models.EmailField(max_length=254),
        ),
    ]