import datetime

from django import forms
from django.utils import timezone
from django.utils.translation import ugettext as _

from .models import Transaction, Income


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('category', 'title', 'amount', 'date')

    def __init__(self, budget=None, creator=None, *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)
        self.budget = budget
        self.creator = creator
        self.fields['title'].widget.attrs['placeholder'] = _('Title...')
        self.fields['amount'].widget.attrs['placeholder'] = _('Amount...')
        return

    def save(self, *args, **kwargs):
        self.instance.budget = self.budget
        self.instance.creator = self.creator
        # who cares about time?..
        self.instance.date = datetime.datetime.combine(self.instance.date, timezone.now().time())
        return super(TransactionForm, self).save(*args, **kwargs)


class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ('category', 'title', 'amount')

    def __init__(self, budget=None, creator=None, *args, **kwargs):
        super(IncomeForm, self).__init__(*args, **kwargs)
        self.budget = budget
        self.creator = creator
        self.fields['title'].widget.attrs['placeholder'] = _('Title...')
        self.fields['amount'].widget.attrs['placeholder'] = _('Amount...')
        return

    def save(self, *args, **kwargs):
        self.instance.budget = self.budget
        self.instance.creator = self.creator
        return super(IncomeForm, self).save(*args, **kwargs)
