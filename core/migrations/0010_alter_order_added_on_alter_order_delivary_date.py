# Generated by Django 5.1.4 on 2025-01-08 05:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_order_orderitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='added_on',
            field=models.DateField(default=datetime.date(2025, 1, 8)),
        ),
        migrations.AlterField(
            model_name='order',
            name='delivary_date',
            field=models.DateField(default=datetime.date(2025, 1, 8)),
        ),
    ]
