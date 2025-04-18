# Generated by Django 5.0 on 2024-11-27 16:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('club', '0002_alter_documentovinculado_options'),
        ('disciplinas', '0002_disciplina_club_profesorcategoria_profesor_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mensaje',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('referencia', models.CharField(max_length=200, unique=True)),
                ('socios_activos', models.BooleanField(default=True)),
                ('fecha', models.DateField(blank=True, null=True)),
                ('texto', models.TextField()),
                ('medio', models.CharField(choices=[('T', 'Telegram'), ('E', 'Email'), ('A', 'Ambos')], default='E', max_length=1)),
                ('estado', models.CharField(choices=[('P', 'Pendiente'), ('E', 'Enviado'), ('C', 'Cancelado')], default='P', max_length=1)),
                ('archivo', models.FileField(blank=True, null=True, upload_to='upload/')),
                ('categoria', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='disciplinas.categoria')),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='club.club')),
                ('disciplina', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='disciplinas.disciplina')),
            ],
            options={
                'verbose_name': 'Mensaje',
                'verbose_name_plural': 'Mensajes',
                'ordering': ['fecha'],
            },
        ),
    ]
