# Generated by Django 5.0.1 on 2024-01-23 10:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0003_alter_uploadmovie_key'),
    ]

    operations = [
        migrations.RenameField(
            model_name='uploadmovie',
            old_name='key',
            new_name='random_key',
        ),
    ]