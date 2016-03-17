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
            name='LoggedTime',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False,
                                        auto_created=True, primary_key=True)),
                ('first_created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('start_date', models.DateField(
                    default=rheia.utils.time.today)),
                ('start_time', models.TimeField(default=None, null=True)),
                ('duration', models.IntegerField(default=None, null=True)),
                ('notes', models.TextField(default=None, max_length=4096,
                                           null=True)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
