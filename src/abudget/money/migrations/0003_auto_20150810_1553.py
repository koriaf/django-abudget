# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('money', '0002_auto_20150810_1326'),
    ]

    operations = [
        migrations.CreateModel(
            name='Income',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('title', models.CharField(max_length=300, blank=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=11)),
                ('date', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('budget', models.ForeignKey(to='money.Budget')),
            ],
            options={
                'ordering': ('-date',),
            },
        ),
        migrations.CreateModel(
            name='IncomeCategory',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('budget', models.ForeignKey(to='money.Budget')),
            ],
        ),
        migrations.AlterModelOptions(
            name='transaction',
            options={'ordering': ('-date',)},
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='income',
        ),
        migrations.AddField(
            model_name='income',
            name='category',
            field=models.ForeignKey(to='money.IncomeCategory'),
        ),
    ]
