from django import forms

from .models import Transaction


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('category', 'title', 'amount')

    def __init__(self, budget=None, *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)
        self.budget = budget
        return

    def save(self, *args, **kwargs):
        self.instance.budget = self.budget
        return super(TransactionForm, self).save(*args, **kwargs)
