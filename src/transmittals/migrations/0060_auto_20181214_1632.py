# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-14 15:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transmittals', '0059_trsrevision_document_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trsrevision',
            name='originator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.Entity', verbose_name='Originator'),
        ),
    ]