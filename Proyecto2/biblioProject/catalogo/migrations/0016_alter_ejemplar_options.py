# Generated by Django 4.0.4 on 2022-06-27 02:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogo', '0015_alter_ejemplar_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ejemplar',
            options={'ordering': ['libro', 'fechaDevolucion'], 'permissions': (('can_mark_returned', 'Establecer libro como devuelto'),)},
        ),
    ]