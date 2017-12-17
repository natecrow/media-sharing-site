# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-16 20:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0004_auto_20171017_0310'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='color',
            field=models.CharField(blank=True, choices=[('RED', 'red'), ('ORANGE', 'orange'), ('YELLOW', 'yellow'), ('GREEN', 'green'), ('TEAL', 'teal'), ('BLUE', 'blue'), ('PURPLE', 'purple'), ('PINK', 'pink'), ('WHITE', 'white'), ('GRAY', 'gray'), ('BLACK', 'black'), ('BROWN', 'brown')], max_length=6),
        ),
    ]