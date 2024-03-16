# Generated by Django 5.0.2 on 2024-03-15 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cuenta', '0012_alter_cuenta_inicio_acceso_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cuenta',
            name='is_staff',
        ),
        migrations.RemoveField(
            model_name='cuenta',
            name='is_superadmin',
        ),
        migrations.AddField(
            model_name='cuenta',
            name='is_user',
            field=models.BooleanField(default=False, verbose_name='Usuario'),
        ),
    ]