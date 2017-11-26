# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-26 13:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tutorial', '0011_auto_20171126_2113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='student',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='students.Student'),
        ),
        migrations.AlterField(
            model_name='session',
            name='tutor',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='tutors.Tutor'),
        ),
    ]