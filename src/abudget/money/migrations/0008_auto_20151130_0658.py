# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('money', '0007_auto_20150816_0629'),
    ]

    operations = [
        migrations.AlterField(
            model_name='budget',
            name='name',
            field=models.CharField(verbose_name='Name', max_length=100),
        ),
        migrations.AlterField(
            model_name='budget',
            name='owner',
            field=models.ForeignKey(related_name='owned_budgets', verbose_name='Owner', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='budget',
            name='users',
            field=models.ManyToManyField(verbose_name='Users', related_name='participated_budgets', blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='income',
            name='amount',
            field=models.DecimalField(decimal_places=2, verbose_name='Amount', max_digits=11),
        ),
        migrations.AlterField(
            model_name='income',
            name='budget',
            field=models.ForeignKey(to='money.Budget', verbose_name='Budget'),
        ),
        migrations.AlterField(
            model_name='income',
            name='category',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.SET_DEFAULT, blank=True, null=True, verbose_name='Income', to='money.IncomeCategory'),
        ),
        migrations.AlterField(
            model_name='income',
            name='creator',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Creator'),
        ),
        migrations.AlterField(
            model_name='income',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date', db_index=True),
        ),
        migrations.AlterField(
            model_name='income',
            name='title',
            field=models.CharField(max_length=300, verbose_name='Title', blank=True),
        ),
        migrations.AlterField(
            model_name='incomecategory',
            name='budget',
            field=models.ForeignKey(to='money.Budget', verbose_name='Budget'),
        ),
        migrations.AlterField(
            model_name='incomecategory',
            name='name',
            field=models.CharField(verbose_name='Name', max_length=200),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='amount',
            field=models.DecimalField(decimal_places=2, verbose_name='Amount', max_digits=11),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='budget',
            field=models.ForeignKey(to='money.Budget', verbose_name='Budget'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='category',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.SET_DEFAULT, blank=True, null=True, verbose_name='Category', to='money.TransactionCategory'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='creator',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Creator'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date', db_index=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='title',
            field=models.CharField(max_length=300, verbose_name='Title', blank=True),
        ),
        migrations.AlterField(
            model_name='transactioncategory',
            name='budget',
            field=models.ForeignKey(to='money.Budget', verbose_name='Budget'),
        ),
        migrations.AlterField(
            model_name='transactioncategory',
            name='name',
            field=models.CharField(verbose_name='Name', max_length=200),
        ),
        migrations.AlterField(
            model_name='transactioncategory',
            name='parent',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.SET_DEFAULT, blank=True, related_name='children', null=True, verbose_name='Parent', to='money.TransactionCategory'),
        ),
    ]
