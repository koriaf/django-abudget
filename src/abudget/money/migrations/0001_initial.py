# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=100)),
                ('owner', models.ForeignKey(related_name='owned_budgets', to=settings.AUTH_USER_MODEL)),
                ('users', models.ManyToManyField(blank=True, related_name='participated_budgets', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('title', models.CharField(blank=True, max_length=300)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=11)),
                ('date', models.DateTimeField(db_index=True, auto_now_add=True)),
                ('budget', models.ForeignKey(to='money.Budget')),
            ],
        ),
        migrations.CreateModel(
            name='TransactionCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=200)),
                ('budget', models.ForeignKey(to='money.Budget')),
                ('parent', models.ForeignKey(null=True, blank=True, to='money.TransactionCategory')),
            ],
        ),
        migrations.AddField(
            model_name='transaction',
            name='category',
            field=models.ForeignKey(null=True, blank=True, to='money.TransactionCategory'),
        ),
    ]
