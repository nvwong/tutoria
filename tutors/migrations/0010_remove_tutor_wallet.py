# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-26 11:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tutors', '0009_auto_20171125_1518'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tutor',
            name='wallet',
        ),
    ]