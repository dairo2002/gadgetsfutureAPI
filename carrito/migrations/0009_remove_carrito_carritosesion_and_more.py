# Generated by Django 5.0.3 on 2024-03-24 00:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carrito', '0008_alter_carritouser_usuario'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carrito',
            name='carritoSesion',
        ),
        migrations.RemoveField(
            model_name='carritouser',
            name='usuario',
        ),
        migrations.RemoveField(
            model_name='carrito',
            name='carritoUser',
        ),
        migrations.RemoveField(
            model_name='carrito',
            name='activo',
        ),
        migrations.RemoveField(
            model_name='carrito',
            name='fecha_agregado',
        ),
        migrations.DeleteModel(
            name='CarritoSesion',
        ),
        migrations.DeleteModel(
            name='CarritoUser',
        ),
    ]
