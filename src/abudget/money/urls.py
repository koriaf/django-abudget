from django.conf.urls import url

from .views import TransactionsView, TransactionsCreateView

urlpatterns = [
    url(r'^$', TransactionsView.as_view(), name='transactions'),
    url(r'^transactions/create/$', TransactionsCreateView.as_view(), name='transaction_create'),
]
