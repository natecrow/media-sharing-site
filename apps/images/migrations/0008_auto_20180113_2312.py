# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-13 23:12
from __future__ import unicode_literals

from django.db import migrations
import tagulous.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0007_auto_20171216_2048'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='category',
        ),
        migrations.RemoveField(
            model_name='image',
            name='color',
        ),
        migrations.AlterField(
            model_name='image',
            name='tags',
            field=tagulous.models.fields.TagField(_set_tag_meta=True, help_text='Enter a comma-separated tag string', to='images.ImageTag'),
        ),
    ]
