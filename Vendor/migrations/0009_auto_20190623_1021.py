# Generated by Django 2.2.2 on 2019-06-23 10:21

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Vendor', '0008_auto_20190623_0450'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='discountExpired',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 6, 24, 10, 21, 54, 488098, tzinfo=utc), null=True),
        ),
    ]
