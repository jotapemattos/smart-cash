# Generated by Django 4.1.7 on 2023-04-26 23:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_veiculo_cliente_id_alter_veiculo_fabricante_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rotativo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_hora_entrada', models.DateTimeField(verbose_name='Entrada')),
                ('data_hora_saida', models.DateTimeField(blank=True, null=True, verbose_name='Saida')),
                ('total', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Total')),
                ('pago', models.BooleanField(default=False, verbose_name='Pago')),
                ('observacoes', models.TextField(blank=True, null=True, verbose_name='Obs. ')),
                ('id_tabela', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.tabelapreco', verbose_name='Preço')),
                ('id_veiculo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.veiculo', verbose_name='Veiculo')),
            ],
            options={
                'verbose_name_plural': 'Rotativos',
            },
        ),
        migrations.CreateModel(
            name='Mensalista',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('observacoes', models.TextField(blank=True, null=True, verbose_name='Obs. ')),
                ('id_tabela', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.tabelapreco', verbose_name='Preco')),
                ('id_veiculo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.veiculo', verbose_name='Veiculo')),
            ],
            options={
                'verbose_name_plural': 'Mensalistas',
            },
        ),
    ]