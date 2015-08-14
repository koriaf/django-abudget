from django.conf.urls import url

from .views import (
    UserSettingsView, UserSettingsCategoryAddView
)

urlpatterns = [
    url(r'^settings/$', UserSettingsView.as_view(), name='settings'),
    url(r'^settings/category_add/$', UserSettingsCategoryAddView.as_view(), name='settings_category_add'),
]
