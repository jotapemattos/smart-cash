# Generated by Django 4.2.2 on 2023-06-18 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_remove_contabancaria_usuario_usuario_contabancaria'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formapagamento',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False, verbose_name='Id pagamento'),
        ),
    ]
