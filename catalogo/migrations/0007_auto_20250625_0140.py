# Generated by Django 2.2 on 2025-06-25 01:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogo', '0006_auto_20250619_1857'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='libroinstancia',
            options={'ordering': ['debidoderegresar'], 'permissions': (('puedeMarcarRetornado', 'Colocar libro como retornado'),)},
        ),
    ]
