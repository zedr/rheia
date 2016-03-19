# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import rheia.utils.time


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=1024)),
                ('first_created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Activities',
            },
        ),
        migrations.CreateModel(
            name='Approval',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('approved', models.DateTimeField(auto_now_add=True)),
                ('approver', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=1024)),
                ('first_created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LoggedTime',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('start_date', models.DateField(default=rheia.utils.time.today)),
                ('start_time', models.TimeField(default=None, null=True)),
                ('duration', models.IntegerField(default=None, null=True)),
                ('notes', models.TextField(default=None, max_length=4096, null=True)),
                ('activity', models.ForeignKey(to='rheia.Activity', null=True)),
                ('client', models.ForeignKey(to='rheia.Client', null=True)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=1024)),
                ('first_created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TaskId',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=1024)),
                ('first_created', models.DateTimeField(auto_now_add=True)),
                ('client', models.ForeignKey(to='rheia.Client', null=True)),
                ('product', models.ForeignKey(to='rheia.Product', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=1024)),
                ('uid', models.CharField(unique=True, max_length=1024, editable=False)),
                ('notes', models.TextField(max_length=4096, blank=True)),
                ('clients', models.ManyToManyField(to='rheia.Client', blank=True)),
                ('leaders', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('members', models.ManyToManyField(related_name='members', to=settings.AUTH_USER_MODEL, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='loggedtime',
            name='product',
            field=models.ForeignKey(to='rheia.Product', null=True),
        ),
        migrations.AddField(
            model_name='loggedtime',
            name='task_id',
            field=models.ForeignKey(to='rheia.TaskId', null=True),
        ),
        migrations.AddField(
            model_name='approval',
            name='time',
            field=models.ForeignKey(to='rheia.LoggedTime'),
        ),
    ]
