# Generated by Django 5.0.6 on 2024-08-22 05:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plan_app', '0009_hotelpayment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookings',
            name='payment_status',
        ),
        migrations.RemoveField(
            model_name='bookings',
            name='stripe_payment_id',
        ),
    ]
