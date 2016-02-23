# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-23 10:21
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
            name='gcUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice_schools_branch_degree', models.CharField(max_length=1000)),
                ('enable_email', models.BooleanField(default=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='resultItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school', models.CharField(max_length=200)),
                ('branch', models.CharField(max_length=200)),
                ('degree', models.CharField(max_length=20)),
                ('stats', models.CharField(max_length=1000)),
                ('via', models.CharField(max_length=200)),
                ('decision', models.CharField(max_length=200)),
                ('time_added', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]