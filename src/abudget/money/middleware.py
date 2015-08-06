from .models import Budget


class ProvideBudgetMiddleware(object):
    def process_request(self, request):
        if request.user.is_authenticated():
            # TODO: right way here
            request.budget = Budget.objects.filter(owner=request.user)[0]
        return
