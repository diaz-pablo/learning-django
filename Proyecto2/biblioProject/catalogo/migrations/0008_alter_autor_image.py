# Generated by Django 4.0.4 on 2022-06-21 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogo', '0007_poi_alter_ejemplar_options_alter_autor_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='autor',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='catalogo/upload/img'),
        ),
    ]
