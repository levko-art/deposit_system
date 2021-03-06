# Generated by Django 2.2.20 on 2021-05-18 10:23

import datetime
from django.db import migrations, models
import django.db.models.expressions


class Migration(migrations.Migration):

    dependencies = [
        ('blockfarm', '0002_auto_20210511_2035'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='program',
            options={'ordering': [django.db.models.expressions.OrderBy(django.db.models.expressions.F('begin_date'), nulls_last=True)]},
        ),
        migrations.AlterField(
            model_name='program',
            name='iteration',
            field=models.DurationField(default=datetime.timedelta(seconds=3600)),
        ),
    ]
