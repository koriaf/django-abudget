from braces.views import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.views.generic import TemplateView, CreateView
from django.shortcuts import redirect

from abudget.money.models import TransactionCategory
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
