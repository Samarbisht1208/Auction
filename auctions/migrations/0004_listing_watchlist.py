# Generated by Django 4.2.6 on 2024-03-12 06:02

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_alter_listing_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='watchlist',
            field=models.ManyToManyField(blank=True, null=True, related_name='listing_watchlist', to=settings.AUTH_USER_MODEL),
        ),
    ]
