# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rheia', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='loggedtime',
            name='notes',
            field=models.TextField(default=None, max_length=4096, null=True),
        ),
    ]
