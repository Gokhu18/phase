# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-14 15:23
from __future__ import unicode_literals

import django.contrib.postgres.fields.hstore
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transmittals', '0058_set_due_dates'),
    ]

    operations = [
        migrations.AddField(
            model_name='trsrevision',
            name='document_data',
            field=django.contrib.postgres.fields.hstore.HStoreField(null=True, verbose_name='Document data'),
        ),
    ]