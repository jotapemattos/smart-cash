# Generated by Django 4.2.2 on 2023-06-18 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_formapagamento_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='conta',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Número da Conta'),
        ),
    ]
