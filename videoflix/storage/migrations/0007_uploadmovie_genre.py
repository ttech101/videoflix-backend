# Generated by Django 5.0.1 on 2024-01-24 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0006_alter_uploadmovie_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadmovie',
            name='genre',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
