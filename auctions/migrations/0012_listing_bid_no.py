# Generated by Django 4.2.6 on 2024-03-15 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_listing_winner'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='bid_no',
            field=models.IntegerField(default=0),
        ),
    ]