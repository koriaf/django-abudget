from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView

urlpatterns = [
    url(r'^$', RedirectView.as_view(pattern_name='money:transactions', permanent=False)),
    url(r'^money/', include('abudget.money.urls', namespace='money')),
    url(r'^users/', include('abudget.users.urls', namespace='users')),
    url(r'^accounts/', include('django.contrib.auth.urls', namespace='accounts')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^i18n/', include('django.conf.urls.i18n')),
]
