from .models import Budget


class ProvideBudgetMiddleware(object):
    def process_request(self, request):
        if request.user.is_authenticated():
            try:
                budget = Budget.objects.get(pk=request.session['budget_id'])
                if not budget.viewable_by(request.user):
                    raise Budget.DoesNotExist()
                request.budget = budget
            except (Budget.DoesNotExist, KeyError, ValueError, TypeError):
                # TODO: if user havent budgets
                request.budget = Budget.objects.filter(owner=request.user)[0]
        return
