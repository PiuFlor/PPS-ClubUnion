# Generated by Django 5.0 on 2024-11-26 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socios', '0002_socio_club'),
    ]

    operations = [
        migrations.AddField(
            model_name='socio',
            name='grupo_telegram',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
