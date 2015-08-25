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
        if self.budget and not self.budget.viewable_by(self.creator):
            raise Exception("Wow")
        self.fields['title'].widget.attrs['placeholder'] = _('Title...')
        self.fields['amount'].widget.attrs['placeholder'] = _('Amount...')
        return

    def clean_category(self, *args, **kwargs):
        category = self.cleaned_data.get('category')
        if category and category.budget != self.budget:
            # TODO
            raise Exception('Wow')
        return category

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

    def __init__(self, budget, creator=None, *args, **kwargs):
        super(IncomeForm, self).__init__(*args, **kwargs)
        self.budget = budget
        self.creator = creator
        if self.budget and not self.budget.viewable_by(self.creator):
            raise Exception("Wow")
        self.fields['title'].widget.attrs['placeholder'] = _('Title...')
        self.fields['amount'].widget.attrs['placeholder'] = _('Amount...')
        self.fields['category'].queryset = self.budget.incomecategory_set.all()
        return

    def clean_category(self, *args, **kwargs):
        category = self.cleaned_data.get('category')
        if category and category.budget != self.budget:
            # TODO
            raise Exception('Wow')
        return category

    def save(self, *args, **kwargs):
        self.instance.budget = self.budget
        self.instance.creator = self.creator
        return super(IncomeForm, self).save(*args, **kwargs)
