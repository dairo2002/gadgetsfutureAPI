# Generated by Django 5.0.1 on 2024-01-31 17:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cuenta', '0004_rename_usuario_cuenta_username'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cuenta',
            old_name='inicio_acceso',
            new_name='date_joined',
        ),
        migrations.RenameField(
            model_name='cuenta',
            old_name='correo_electronico',
            new_name='email',
        ),
        migrations.RenameField(
            model_name='cuenta',
            old_name='apellido',
            new_name='first_name',
        ),
        migrations.RenameField(
            model_name='cuenta',
            old_name='nombre',
            new_name='last_name',
        ),
        migrations.RenameField(
            model_name='cuenta',
            old_name='telefono',
            new_name='phone',
        ),
    ]
