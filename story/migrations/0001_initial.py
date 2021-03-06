# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-01 10:48
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=250)),
                ('article_title', models.CharField(max_length=500)),
                ('genre', models.CharField(max_length=100)),
                ('article_pic', models.FileField(upload_to='')),
                ('parts', models.IntegerField(default=0)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('part_title', models.CharField(max_length=250)),
                ('file', models.FileField(upload_to='')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='story.Article')),
            ],
        ),
    ]
