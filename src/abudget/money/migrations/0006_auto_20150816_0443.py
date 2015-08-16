# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('money', '0005_auto_20150814_1741'),
    ]

    operations = [
        migrations.AlterField(
            model_name='income',
            name='date',
            field=models.DateTimeField(default=datetime.datetime.now, db_index=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='date',
            field=models.DateTimeField(default=datetime.datetime.now, db_index=True),
        ),
        migrations.AlterField(
            model_name='transactioncategory',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_DEFAULT, related_name='children', to='money.TransactionCategory', default=None, null=True, blank=True),
        ),
    ]
