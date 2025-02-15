# Generated by Django 5.1.4 on 2025-01-08 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_alter_order_added_on_alter_order_delivary_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('processing', 'Processing'), ('shipped', 'Shipped'), ('delivered', 'Delivered')], default='created', max_length=20),
        ),
    ]
