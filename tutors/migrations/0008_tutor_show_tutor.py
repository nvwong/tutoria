# -*- coding: utf-8 -*-
<<<<<<< HEAD
# Generated by Django 1.11.6 on 2017-11-24 13:08
=======
# Generated by Django 1.11.6 on 2017-11-23 13:13
>>>>>>> edd8d2b5c09561f77743bc925614bcaa2cbd3f92
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutors', '0007_auto_20171119_1453'),
    ]

    operations = [
        migrations.AddField(
            model_name='tutor',
            name='show_tutor',
            field=models.BooleanField(default=True),
        ),
    ]
