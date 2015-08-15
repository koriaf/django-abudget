from braces.views import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.db import models
from django.views.generic import TemplateView, CreateView
from django.shortcuts import redirect

from abudget.money.models import TransactionCategory, Transaction
from abudget.money.views import FilterByDateMixin
from abudget.users.forms import CreateTransactionCategoryForm


class UserSettingsView(LoginRequiredMixin, TemplateView):
    template_name = 'users/settings.html'

    def post(self, request, *args, **kwargs):
        if 'delete_category' in request.POST:
            category_id = request.POST.get('delete_category')
            category = TransactionCategory.objects.get(
                budget=request.budget,
                id=category_id
            )
            for child in category.children.all():
                child.parent = category.parent
                child.save()
            category.delete()
            messages.success(request, 'Category deleted')
        return redirect(reverse('users:settings'))


class UserSettingsCategoryAddView(LoginRequiredMixin, CreateView):
    model = TransactionCategory
    form_class = CreateTransactionCategoryForm

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super(UserSettingsCategoryAddView, self).get_form_kwargs(*args, **kwargs)
        form_kwargs['budget'] = self.request.budget
        return form_kwargs

    def get_success_url(self):
        return reverse('users:settings')


class UserStatView(LoginRequiredMixin, FilterByDateMixin, TemplateView):
    template_name = 'users/stat.html'

    def get_spent_by_category_report_data(self):
        this_period_transactions = Transaction.objects.filter(
            budget=self.request.budget,
        )
        this_period_transactions = self.filter_queryset_by_date(this_period_transactions)
        categories = self.request.budget.get_ordered_categories_list()
        for category in categories:
            category.report_data = {
                'transactions_count': this_period_transactions.filter(category=category).count(),
                'transactions_amount': this_period_transactions.filter(
                    category=category
                ).aggregate(models.Sum('amount'))['amount__sum'] or 0,
            }
        categories = sorted(categories, key=lambda x: x.report_data['transactions_amount'], reverse=True)
        return categories

    def get_context_data(self, *args, **kwargs):
        context = super(UserStatView, self).get_context_data(*args, **kwargs)
        context['spent_by_category_report_data'] = self.get_spent_by_category_report_data()
        return context
