# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-05-23 05:44
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('story', '0012_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='like',
            name='is_like',
        ),
    ]
