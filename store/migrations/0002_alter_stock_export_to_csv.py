# Generated by Django 5.1 on 2024-08-19 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='export_to_CSV',
            field=models.BooleanField(default=False),
        ),
    ]
