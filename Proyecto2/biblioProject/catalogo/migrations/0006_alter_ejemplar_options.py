# Generated by Django 4.0.4 on 2022-07-03 22:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogo', '0005_alter_customuser_first_name_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ejemplar',
            options={'ordering': ['libro', 'fechaDevolucion'], 'permissions': (('can_reserve_a_copy', 'Puede reservar ejemplar'), ('can_cancel_reservation', 'Puede cancelar reserva'), ('can_view_my_loans', 'Puedo ver mis prestamos'))},
        ),
    ]
