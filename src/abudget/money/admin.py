from django.contrib import admin

from .models import Budget, TransactionCategory, Transaction, IncomeCategory, Income


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'name')


@admin.register(TransactionCategory)
class TransactionCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'budget', 'parent', 'name')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'budget', 'title', 'amount', 'date')


admin.site.register(IncomeCategory)
admin.site.register(Income)
