from django import forms

from abudget.money.models import TransactionCategory


class CreateTransactionCategoryForm(forms.ModelForm):
    class Meta:
        model = TransactionCategory
        fields = ('name', 'parent')

    def __init__(self, budget=None, *args, **kwargs):
        super(CreateTransactionCategoryForm, self).__init__(*args, **kwargs)
        self.budget = budget
        return

    def save(self, *args, **kwargs):
        self.instance.budget = self.budget
        return super(CreateTransactionCategoryForm, self).save(*args, **kwargs)
