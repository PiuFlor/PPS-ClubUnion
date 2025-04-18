# Generated by Django 5.0 on 2024-11-25 18:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('parametros', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Disciplina',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, unique=True, verbose_name='Disciplina')),
                ('estado', models.BooleanField(default=True, verbose_name='¿Está activo?')),
                ('monto', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Caja')),
            ],
            options={
                'verbose_name': 'Disciplina',
                'verbose_name_plural': 'Disciplinas',
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, verbose_name='Categoría')),
                ('anio', models.IntegerField(default=2024, verbose_name='Año')),
                ('estado', models.BooleanField(default=True, verbose_name='¿Está activo?')),
                ('edad_desde', models.PositiveIntegerField()),
                ('edad_hasta', models.PositiveIntegerField()),
                ('disciplina', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='disciplinas.disciplina', verbose_name='Disciplina')),
            ],
            options={
                'verbose_name': 'Categoria',
                'verbose_name_plural': 'Categorias',
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='Horario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dia_semana', models.CharField(blank=True, choices=[('LU', 'Lunes'), ('MA', 'Martes'), ('MI', 'Miércoles'), ('JU', 'Jueves'), ('VI', 'Viernes'), ('SA', 'Sábado'), ('DO', 'Domingo')], max_length=255, null=True, verbose_name='Día de la Semana')),
                ('inicio', models.TimeField(help_text='Formato requerido: HH:MM (ejemplo: 17:30)')),
                ('fin', models.TimeField(help_text='Formato requerido: HH:MM (ejemplo: 18:30)')),
                ('cancha', models.ForeignKey(limit_choices_to={'apto_deporte': True}, on_delete=django.db.models.deletion.CASCADE, to='parametros.espacio', verbose_name='Cancha')),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='disciplinas.categoria', verbose_name='Categoria')),
            ],
            options={
                'verbose_name': 'Horario',
                'verbose_name_plural': 'Horarios',
                'ordering': ['dia_semana', 'inicio'],
            },
        ),
        migrations.CreateModel(
            name='ProfesorCategoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.BooleanField(default=True, verbose_name='¿Está activo?')),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Categoria_profesor', to='disciplinas.categoria')),
            ],
            options={
                'verbose_name': 'Profesor Categoria',
                'verbose_name_plural': 'Profesores Categoria',
            },
        ),
        migrations.CreateModel(
            name='SocioCategoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.BooleanField(default=True, verbose_name='¿Está activo?')),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Categoria_socio', to='disciplinas.categoria')),
            ],
            options={
                'verbose_name': 'Socio Categoria',
                'verbose_name_plural': 'Socios Categoria',
            },
        ),
        migrations.AddConstraint(
            model_name='categoria',
            constraint=models.UniqueConstraint(fields=('nombre', 'disciplina', 'anio'), name='unique_categoria_disciplina_anio'),
        ),
    ]
