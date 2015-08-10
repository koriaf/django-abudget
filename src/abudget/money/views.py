from braces.views import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.db.models import Sum
from django.http import HttpResponse
from django.views.generic import TemplateView, CreateView, View

from .forms import TransactionForm
from .models import Transaction, Income


class TransactionsView(LoginRequiredMixin, TemplateView):
    template_name = 'money/transactions.html'

    def get_context_data(self, *args, **kwargs):
        context = super(TransactionsView, self).get_context_data(*args, **kwargs)

        stat_spent = Transaction.objects.filter(
            budget=self.request.budget,
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        stat_income = Income.objects.filter(
            budget=self.request.budget,
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        stat_balance = stat_income - stat_spent

        context['stat_spent'] = stat_spent
        context['stat_income'] = stat_income
        context['stat_balance'] = stat_balance

        context['new_transaction_form'] = TransactionForm()
        context['transactions'] = Transaction.objects.filter(
            budget=self.request.budget,
        )
        return context


class TransactionsCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'money/transactions.html'

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super(TransactionsCreateView, self).get_form_kwargs(*args, **kwargs)

        # TODO: right workflow here
        # TODO: error handling here
        form_kwargs['budget'] = self.request.budget
        return form_kwargs

    def get_success_url(self):
        return reverse('money:transactions')


class TransactionsRemoveView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        transaction = Transaction.objects.get(
            id=request.POST.get('transaction_id'),
            budget=request.budget
        )
        transaction.delete()
        return HttpResponse('ok')


class IncomeView(LoginRequiredMixin, TemplateView):
    template_name = 'money/income.html'
