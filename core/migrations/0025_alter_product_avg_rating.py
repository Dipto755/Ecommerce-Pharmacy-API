# Generated by Django 5.1.4 on 2025-01-13 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_rename_delivary_date_order_delivery_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='avg_rating',
            field=models.FloatField(blank=True, default=0),
        ),
    ]
