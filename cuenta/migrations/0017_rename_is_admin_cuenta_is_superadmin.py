# Generated by Django 5.0.2 on 2024-03-15 20:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cuenta', '0016_remove_cuenta_is_superadmin'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cuenta',
            old_name='is_admin',
            new_name='is_superadmin',
        ),
    ]
