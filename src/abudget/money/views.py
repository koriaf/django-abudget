import datetime
import json

from braces.views import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.db.models import Sum
from django.http import HttpResponse
from django.views.generic import TemplateView, CreateView, View
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.translation import ugettext as _

from .forms import TransactionForm, IncomeForm
from .models import Transaction, Income, DEFAULT_FILTER_BY_DATE


class TransactionsView(LoginRequiredMixin, TemplateView):
    template_name = 'money/transactions.html'

    def get_context_data(self, *args, **kwargs):
        context = super(TransactionsView, self).get_context_data(*args, **kwargs)

        stat_spent = Transaction.objects.filter_by_date(self.request).filter(
            budget=self.request.budget,
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        stat_income = Income.objects.filter_by_date(self.request).filter(
            budget=self.request.budget,
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        stat_balance = stat_income - stat_spent

        context['stat_spent'] = stat_spent
        context['stat_income'] = stat_income
        context['stat_balance'] = stat_balance

        transactions = Transaction.objects.filter_by_date(self.request).filter(
            budget=self.request.budget,
        )

        context['new_transaction_form'] = TransactionForm()
        context['transactions'] = transactions
        return context


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

    def get_context_data(self, *args, **kwargs):
        context = super(IncomeView, self).get_context_data(*args, **kwargs)

        context['new_income_form'] = IncomeForm(budget=self.request.budget, creator=self.request.user)
        context['transactions'] = Income.objects.filter_by_date(self.request).filter(
            budget=self.request.budget,
        )
        return context


class IncomeCreateView(LoginRequiredMixin, CreateView):
    model = Income
    form_class = IncomeForm
    # TODO: exception if form invalid

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super(IncomeCreateView, self).get_form_kwargs(*args, **kwargs)
        # TODO: right workflow here
        # TODO: error handling here
        form_kwargs['budget'] = self.request.budget
        form_kwargs['creator'] = self.request.user
        return form_kwargs

    def get_success_url(self):
        return reverse('money:income')


class UpdateFilterView(View):
    '''
    Sets request.session.filter_by corresponding to user input - date range, in fact
    '''

    def post(self, request, *args, **kwargs):
        redirect_url = request.POST.get('redirect_to')
        today = timezone.now().date()

        filter_by = request.session.get('filter_by', DEFAULT_FILTER_BY_DATE)
        filter_by_date = request.POST.get('date', 'this_month')

        first_day = None
        last_day = None

        if filter_by_date == 'this_month':
            first_day = today.replace(day=1)
            last_day = (first_day + datetime.timedelta(days=45)).replace(day=1) - datetime.timedelta(days=1)
        elif filter_by_date == 'prev_month':
            last_day = today.replace(day=1) - datetime.timedelta(days=1)
            first_day = (last_day - datetime.timedelta(days=10)).replace(day=1)
        elif filter_by_date == 'date_custom':
            # disallow wrong data.
            # TODO: client-side date check
            try:
                first_day = datetime.datetime.strptime(request.POST.get('date_from'), "%Y-%m-%d")
            except (ValueError, TypeError):
                first_day = timezone.now().date()
            try:
                last_day = datetime.datetime.strptime(request.POST.get('date_to'), "%Y-%m-%d")
            except (ValueError, TypeError):
                last_day = timezone.now().date()

        filter_by['date'] = filter_by_date
        if first_day:
            first_day = first_day.strftime("%Y-%m-%d")
        if last_day:
            last_day = last_day.strftime("%Y-%m-%d")
        filter_by['date_from'] = first_day
        filter_by['date_to'] = last_day

        request.session['filter_by'] = filter_by
        request.session.modified = True
        if not redirect_url[0] == '/':
            raise Exception()
        return redirect(redirect_url)


class IncomeRemoveView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        transaction = Income.objects.get(
            id=request.POST.get('transaction_id'),
            budget=request.budget
        )
        transaction.delete()
        return HttpResponse('ok')


class TransactionsCreateAjaxView(LoginRequiredMixin, View):
    def render(self, data):
        return HttpResponse(
            json.dumps(data),
            content_type='application/json'
        )

    def post(self, request, *args, **kwargs):
        result = {
            'status': 'error',
            'message': 'Internal programming error',
            'data': None
        }
        form = TransactionForm(
            data=request.POST,
            budget=request.budget,
            creator=request.user
        )
        if form.is_valid():
            new_trans = form.save()
            result['status'] = 'success'
            result['message'] = _('Transaction added')
            result['data'] = new_trans.get_json_repr()
        else:
            errors = []
            for e in form.errors.values():
                errors.append(e[0])
            result['message'] = 'Error: {}'.format(
                ', '.join(errors)
            )
            result['data'] = form.errors
        return self.render(result)
