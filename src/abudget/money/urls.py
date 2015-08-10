from django.conf.urls import url

from .views import TransactionsView, TransactionsCreateView, TransactionsRemoveView, IncomeView

urlpatterns = [
    url(r'^$', TransactionsView.as_view(), name='transactions'),
    url(r'^income/$', IncomeView.as_view(), name='income'),
    url(r'^transactions/create/$', TransactionsCreateView.as_view(), name='transaction_create'),
    url(r'^transactions/remove/$', TransactionsRemoveView.as_view(), name='transaction_remove'),
]
