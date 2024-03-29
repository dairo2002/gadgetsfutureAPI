# Generated by Django 5.0.1 on 2024-01-27 17:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tienda', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Carrito',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('carrito_sesion', models.CharField(blank=True, max_length=250)),
                ('cantidad', models.IntegerField()),
                ('activo', models.BooleanField(default=True)),
                ('fecha_agregado', models.DateField(auto_now_add=True)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tienda.producto')),
            ],
        ),
    ]
