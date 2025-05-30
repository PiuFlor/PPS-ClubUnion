# Generated by Django 5.0 on 2024-12-10 20:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0003_remove_participantesevento_nombre_and_more'),
        ('parametros', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evento',
            name='ciudad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parametros.ciudad', verbose_name='Ciudad'),
        ),
        migrations.AlterField(
            model_name='evento',
            name='estado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parametros.estado', verbose_name='Estado'),
        ),
        migrations.AlterField(
            model_name='evento',
            name='tipo_evento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parametros.tipoevento', verbose_name='Tipo_evento'),
        ),
    ]
