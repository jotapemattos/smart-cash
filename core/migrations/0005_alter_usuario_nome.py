# Generated by Django 4.2.2 on 2023-06-18 01:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_usuario_contabancaria'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='nome',
            field=models.CharField(blank=True, max_length=45, null=True, verbose_name='Nome'),
        ),
    ]
