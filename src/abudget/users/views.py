import datetime

from braces.views import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.db import models
from django.views.generic import TemplateView, CreateView, View
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.translation import ugettext as _

from abudget.money.models import TransactionCategory, Transaction, Income, Budget
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

    def get_context_data(self, *args, **kwargs):
        context = super(UserSettingsView, self).get_context_data(*args, **kwargs)
        context['budgets'] = Budget.objects.filter(
            models.Q(users__in=[self.request.user]) | models.Q(owner=self.request.user)
        )
        return context


class UserSettingsCategoryAddView(LoginRequiredMixin, CreateView):
    model = TransactionCategory
    form_class = CreateTransactionCategoryForm

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super(UserSettingsCategoryAddView, self).get_form_kwargs(*args, **kwargs)
        form_kwargs['budget'] = self.request.budget
        return form_kwargs

    def get_success_url(self):
        return reverse('users:settings')


class UserStatView(LoginRequiredMixin, TemplateView):
    template_name = 'users/stat.html'

    def get_spent_by_category_report_data(self):
        this_period_transactions = Transaction.objects.filter_by_date(self.request).filter(
            budget=self.request.budget,
        )
        categories = self.request.budget.get_ordered_categories_list() + [
            TransactionCategory(
                id=None,
                name=_('Without category')
            )
        ]
        for category in categories:
            this_category_transactions = this_period_transactions.filter(category_id=category.id)
            category.report_data = {
                'transactions': this_category_transactions,
                'transactions_count': this_category_transactions.count(),
                'transactions_amount': this_category_transactions.aggregate(
                    models.Sum('amount')
                )['amount__sum'] or 0,
            }

        # TODO: transactions without category
        categories = sorted(categories, key=lambda x: x.report_data['transactions_amount'], reverse=True)
        return categories

    def get_total_amounts(self):
        stat_spent = Transaction.objects.filter_by_date(self.request).filter(
            budget=self.request.budget,
        ).aggregate(models.Sum('amount'))['amount__sum'] or 0

        stat_income = Income.objects.filter_by_date(self.request).filter(
            budget=self.request.budget,
        ).aggregate(models.Sum('amount'))['amount__sum'] or 0

        stat_balance = stat_income - stat_spent
        return {
            'stat_spent': stat_spent,
            'stat_income': stat_income,
            'stat_balance': stat_balance,
        }

    def get_data_by_months(self):
        months = []
        today = timezone.now().date().replace(day=15)
        year_ago = today - datetime.timedelta(days=365)
        while today > year_ago:
            month_data = {
                'name': today.strftime("%B %Y"),
                'income': Income.objects.filter(
                    budget=self.request.budget,
                    date__year=today.year,
                    date__month=today.month,
                ).aggregate(models.Sum('amount'))['amount__sum'] or 0,
                'spent': Transaction.objects.filter(
                    budget=self.request.budget,
                    date__year=today.year,
                    date__month=today.month,
                ).aggregate(models.Sum('amount'))['amount__sum'] or 0,
                'balance': 0,
            }
            month_data['balance'] = month_data['income'] - month_data['spent']
            month_data['income'] = round(month_data['income'])
            month_data['spent'] = round(month_data['spent'])
            month_data['balance'] = round(month_data['balance'])
            months.append(month_data)
            today -= datetime.timedelta(
                days=30
            )
        return months

    def get_context_data(self, *args, **kwargs):
        context = super(UserStatView, self).get_context_data(*args, **kwargs)
        context['spent_by_category_report_data'] = self.get_spent_by_category_report_data()
        context['total_amounts'] = self.get_total_amounts()
        context['data_by_months'] = self.get_data_by_months()
        return context


class BudgetActivateView(LoginRequiredMixin, View):
    def post(self, *args, **kwargs):
        try:
            budget = Budget.objects.get(
                pk=self.request.POST['budget']
            )
            if not budget.viewable_by(self.request.user):
                raise Budget.DoesNotExist()
            self.request.session['budget_id'] = budget.id
        except Budget.DoesNotExist:
            pass
        return redirect('users:settings')
