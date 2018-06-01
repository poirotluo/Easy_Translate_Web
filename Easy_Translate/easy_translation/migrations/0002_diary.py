# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-04-03 04:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('easy_translation', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='diary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('text', models.CharField(max_length=500)),
                ('dtime', models.DateTimeField(auto_now=True)),
                ('User_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='easy_translation.user_info')),
            ],
        ),
    ]