# Generated by Django 5.0.1 on 2024-02-14 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('galeria', '0005_fotografia_usuario_alter_fotografia_foto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fotografia',
            name='publicada',
            field=models.BooleanField(default=True),
        ),
    ]