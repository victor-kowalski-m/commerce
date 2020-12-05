# Generated by Django 3.1.3 on 2020-11-19 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_bid_comment_listing'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='category',
            field=models.CharField(blank=True, max_length=64),
        ),
        migrations.AlterField(
            model_name='listing',
            name='image_url',
            field=models.URLField(blank=True, max_length=2000),
        ),
    ]