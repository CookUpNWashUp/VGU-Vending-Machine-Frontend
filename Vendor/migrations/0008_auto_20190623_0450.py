# Generated by Django 2.2.2 on 2019-06-23 04:50

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Vendor', '0007_auto_20190623_0443'),
    ]

    operations = [
        migrations.RenameField(
            model_name='slot',
            old_name='slot',
            new_name='slotNr',
        ),
        migrations.AlterField(
            model_name='discount',
            name='discountExpired',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 6, 24, 4, 50, 17, 659034, tzinfo=utc), null=True),
        ),
    ]
