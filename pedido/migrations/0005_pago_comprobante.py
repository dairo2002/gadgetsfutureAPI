# Generated by Django 5.0.1 on 2024-02-13 00:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedido', '0004_rename_estado_pago_estado_pago_alter_pago_fecha_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pago',
            name='comprobante',
            field=models.ImageField(blank=True, upload_to='comprobante_pago/'),
        ),
    ]
