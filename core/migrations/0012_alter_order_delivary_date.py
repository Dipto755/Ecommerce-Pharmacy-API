# Generated by Django 5.1.4 on 2025-01-08 05:41

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_alter_order_added_on_alter_order_delivary_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivary_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
