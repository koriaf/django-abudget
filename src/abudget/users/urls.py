from django.conf.urls import url

from .views import (
    UserSettingsView, UserSettingsCategoryAddView,
    UserStatView,
    BudgetActivateView,
)

urlpatterns = [
    url(r'^settings/$', UserSettingsView.as_view(), name='settings'),
    url(r'^settings/category_add/$', UserSettingsCategoryAddView.as_view(), name='settings_category_add'),
    url(r'^settings/budget/activate/$', BudgetActivateView.as_view(), name='settings_budget_activate'),

    url(r'^stat/$', UserStatView.as_view(), name='stat'),
]
