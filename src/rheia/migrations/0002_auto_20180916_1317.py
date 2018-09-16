# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('rheia', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='taskid',
            options={'verbose_name': 'Task', 'verbose_name_plural': 'Tasks'},
        ),
        migrations.AlterField(
            model_name='loggedtime',
            name='duration',
            field=models.IntegerField(null=True, help_text='The quantity of time to log, in seconds.', default=None),
        ),
        migrations.AlterField(
            model_name='team',
            name='leaders',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='leaders'),
        ),
    ]
