# Generated by Django 4.2.6 on 2024-03-12 16:39

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_listing_watchlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='watchlist',
            field=models.ManyToManyField(blank=True, null=True, related_name='listing_watchlist_related_name', to=settings.AUTH_USER_MODEL),
        ),
    ]
