# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-03-12 11:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mode', models.IntegerField()),
                ('date', models.DateField(blank=True, null=True)),
            ],
        ),
    ]
