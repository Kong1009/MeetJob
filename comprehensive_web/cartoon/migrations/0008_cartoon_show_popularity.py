# Generated by Django 4.1.3 on 2023-01-11 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cartoon', '0007_alter_cartoon_popularity'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartoon',
            name='show_popularity',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
