# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('money', '0004_auto_20150810_1601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='income',
            name='category',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='money.IncomeCategory', null=True, default=None),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='category',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='money.TransactionCategory', null=True, default=None),
        ),
        migrations.AlterField(
            model_name='transactioncategory',
            name='parent',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='money.TransactionCategory', null=True, default=None),
        ),
    ]
