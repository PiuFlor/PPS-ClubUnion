# Generated by Django 5.0 on 2024-12-09 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cuotas', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pago',
            options={'ordering': ['fecha'], 'verbose_name': 'Pago', 'verbose_name_plural': 'Pagos'},
        ),
        migrations.RenameField(
            model_name='pago',
            old_name='fecha_pago',
            new_name='fecha',
        ),
        migrations.RenameField(
            model_name='pago',
            old_name='monto_pagado',
            new_name='monto',
        ),
        migrations.RemoveField(
            model_name='pago',
            name='cuotas_canceladas',
        ),
        migrations.RemoveField(
            model_name='pago',
            name='modalidad_pago',
        ),
        migrations.AddField(
            model_name='pago',
            name='detalles',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pago',
            name='estado',
            field=models.CharField(choices=[('pendiente', 'Pendiente'), ('confirmado', 'Confirmado')], default='pendiente', max_length=15),
        ),
        migrations.AddField(
            model_name='pago',
            name='modalidad',
            field=models.CharField(choices=[('efectivo', 'Efectivo'), ('transferencia', 'Transferencia'), ('otros', 'Otros')], default='efectivo', max_length=20),
        ),
        migrations.AddField(
            model_name='pago',
            name='referencia',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
