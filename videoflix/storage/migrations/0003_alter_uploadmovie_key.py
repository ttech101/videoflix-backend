# Generated by Django 5.0.1 on 2024-01-23 10:46

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0002_uploadmovie_big_picture_uploadmovie_cover_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadmovie',
            name='key',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
