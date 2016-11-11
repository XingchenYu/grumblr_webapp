# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-18 00:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0016_auto_20161015_1848'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='blog',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='com_user',
        ),
        migrations.AddField(
            model_name='blog',
            name='last_changed',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
    ]