from django.db import models
from django.conf import settings


class Budget(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='owned_budgets')
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='participated_budgets')

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return '{} ({})'.format(self.name, self.owner)

    def get_toplevel_categories(self):
        return TransactionCategory.objects.filter(
            budget=self,
            parent=None
        )

    def get_ordered_categories_list(self):
        result = []
        top_level_categories = self.transactioncategory_set.filter(
            parent=None
        )
        for topcat in top_level_categories:
            result.append(topcat)
            result += topcat.get_subcategories_recursive_list()
        return result


class TransactionCategory(models.Model):
    budget = models.ForeignKey('Budget')
    parent = models.ForeignKey('self', blank=True, null=True)
    name = models.CharField(max_length=200)
    # TODO: orderable

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.get_title()
        # return '[{}#{}] {}'.format(self.budget.id, self.budget.name, self.get_title())

    def get_title(self):
        if self.parent:
            return '{} → {}'.format(self.parent.get_title(), self.name)
        else:
            return self.name

    def get_subcategories_recursive_list(self):
        result = []
        subcategories_first_level = TransactionCategory.objects.filter(
            parent=self
        )
        for subcat in subcategories_first_level:
            result.append(subcat)
            result += subcat.get_subcategories_recursive_list()
        return result


class Transaction(models.Model):
    budget = models.ForeignKey('Budget')
    category = models.ForeignKey('TransactionCategory', blank=True, null=True)
    title = models.CharField(max_length=300, blank=True)
    amount = models.DecimalField(max_digits=11, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return '[{}#{}] {} at {}'.format(self.budget.id, self.budget.name, self.amount, self.date)
