# Generated by Django 5.0.6 on 2024-08-16 08:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plan_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='homestays',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
