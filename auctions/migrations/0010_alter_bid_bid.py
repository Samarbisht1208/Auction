# Generated by Django 4.2.6 on 2024-03-13 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_alter_bid_bid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='bid',
            field=models.FloatField(default=0),
        ),
    ]
