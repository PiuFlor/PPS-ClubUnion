# Generated by Django 5.0 on 2024-12-09 20:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0002_alter_participantesevento_options_and_more'),
        ('socios', '0004_alter_socio_email_contacto_escolar_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='participantesevento',
            name='nombre',
        ),
        migrations.AddField(
            model_name='participantesevento',
            name='socios',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='socio_participantes', to='socios.socio'),
            preserve_default=False,
        ),
    ]
