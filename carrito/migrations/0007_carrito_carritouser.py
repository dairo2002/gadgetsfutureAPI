# Generated by Django 5.0.3 on 2024-03-23 17:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carrito', '0006_carritouser'),
    ]

    operations = [
        migrations.AddField(
            model_name='carrito',
            name='carritoUser',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='carrito.carritouser'),
            preserve_default=False,
        ),
    ]
