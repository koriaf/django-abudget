from braces.views import LoginRequiredMixin
from django.views.generic import TemplateView, CreateView
from django.core.urlresolvers import reverse

from .forms import TransactionForm
from .models import Transaction


class TransactionsView(LoginRequiredMixin, TemplateView):
    template_name = 'money/transactions.html'

    def get_context_data(self, *args, **kwargs):
        context = super(TransactionsView, self).get_context_data(*args, **kwargs)
        context['new_transaction_form'] = TransactionForm()
        context['transactions'] = Transaction.objects.filter(
            budget=self.request.budget
        )
        return context


class TransactionsCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'money/transactions.html'

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super(TransactionsCreateView, self).get_form_kwargs(*args, **kwargs)

        # TODO: right workflow here
        form_kwargs['budget'] = self.request.budget
        return form_kwargs

    def get_success_url(self):
        return reverse('money:transactions')
