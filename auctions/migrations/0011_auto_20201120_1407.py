# Generated by Django 3.1.3 on 2020-11-20 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_auto_20201120_1359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.CharField(max_length=50, null=True),
        ),
    ]