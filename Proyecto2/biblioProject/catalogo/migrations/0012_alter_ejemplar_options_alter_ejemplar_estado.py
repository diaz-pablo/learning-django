# Generated by Django 4.0.4 on 2022-06-24 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogo', '0011_alter_libro_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ejemplar',
            options={'ordering': ['libro', 'fechaDevolucion']},
        ),
        migrations.AlterField(
            model_name='ejemplar',
            name='estado',
            field=models.CharField(choices=[('m', 'en Mantenimiento'), ('p', 'Prestado'), ('d', 'Disponible'), ('r', 'Reservado')], default='d', help_text='Disponibilidad del Ejemplar', max_length=1),
        ),
    ]