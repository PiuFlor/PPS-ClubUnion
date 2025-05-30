# Generated by Django 5.0 on 2024-12-02 13:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('club', '0003_club_grupo_telegram'),
        ('indumentaria', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='articulo',
            name='club',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='club.club'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='detalleentrega',
            name='club',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='club.club'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='detallerecepcion',
            name='club',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='club.club'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='entrega',
            name='club',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='club.club'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='recepcion',
            name='club',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='club.club'),
            preserve_default=False,
        ),
    ]
