# Generated by Django 5.0.1 on 2024-02-13 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedido', '0005_pago_comprobante'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pago',
            name='metodo_pago',
            field=models.CharField(choices=[('Efectivo', 'Efectivo'), ('Nequi', 'Nequi')], max_length=50),
        ),
    ]
