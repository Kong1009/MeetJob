# Generated by Django 4.1.3 on 2023-01-05 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_alter_product_info'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='info',
            field=models.TextField(blank=True, null=True),
        ),
    ]
