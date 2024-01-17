# Generated by Django 5.0.1 on 2024-01-17 06:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='last_logged_in',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='author_userprofile_set', to=settings.AUTH_USER_MODEL),
        ),
    ]
