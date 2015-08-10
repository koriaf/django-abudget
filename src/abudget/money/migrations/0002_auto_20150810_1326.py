# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('money', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='transactioncategory',
            options={'ordering': ('id',)},
        ),
        migrations.AddField(
            model_name='transaction',
            name='income',
            field=models.BooleanField(default=False),
        ),
    ]
