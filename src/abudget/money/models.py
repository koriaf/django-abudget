import datetime

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

# TODO: it's bad bad place for this, move it somewhere
DEFAULT_FILTER_BY_DATE = {
    'date': 'this_month',
    'date_from': None,
    'date_to': None,
}


class Budget(models.Model):
    name = models.CharField(_('Name'), max_length=100)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Owner'), related_name='owned_budgets')
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Users'),
        blank=True,
        related_name='participated_budgets'
    )

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return '{} ({})'.format(self.name, self.owner)

    def get_toplevel_categories(self):
        return TransactionCategory.objects.filter(
            budget=self,
            parent=None
        )

    def get_ordered_categories_list(self):
        result = []
        top_level_categories = self.transactioncategory_set.filter(
            parent=None
        )
        for topcat in top_level_categories:
            result.append(topcat)
            result += topcat.get_subcategories_recursive_list()
        return result

    def viewable_by(self, user):
        if self.owner != user and user not in self.users:
            # TODO: add logging here
            return False
        return True


class TransactionBase(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Creator'))
    budget = models.ForeignKey('Budget', verbose_name=_('Budget'))
    title = models.CharField(_('Title'), max_length=300, blank=True)
    amount = models.DecimalField(_('Amount'), max_digits=11, decimal_places=2)
    date = models.DateTimeField(_('Date'), db_index=True, default=timezone.now)

    class Meta:
        abstract = True


class TransactionCategory(models.Model):
    # TODO: orderable
    budget = models.ForeignKey('Budget', verbose_name=_('Budget'))
    parent = models.ForeignKey(
        'self',
        verbose_name=_('Parent'),
        blank=True, null=True, default=None,
        on_delete=models.SET_DEFAULT,
        related_name='children',
    )
    name = models.CharField(_('Name'), max_length=200)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.get_title()

    def get_title(self):
        if self.parent:
            return '{} → {}'.format(self.parent.get_title(), self.name)
        else:
            return self.name

    def get_subcategories_recursive_list(self, level=1):
        result = []
        subcategories_first_level = TransactionCategory.objects.filter(
            parent=self
        )
        for subcat in subcategories_first_level:
            subcat.level = level
            result.append(subcat)
            result += subcat.get_subcategories_recursive_list(level + 1)
        return result

    def save(self, *args, **kwargs):
        if self.parent and self.parent.budget != self.budget:
            raise Exception("Parent category budget not equal to self budget for {}!".format(self))
        return super(TransactionCategory, self).save(*args, **kwargs)


class FilterByDateManager(models.Manager):
    def filter_by_date(self, request):
        'filter out all objects, which have date not in range from request.session.filter_by'
        queryset = self.get_queryset()
        current_timezone = timezone.get_current_timezone()
        filter_by = request.session.get(
            'filter_by',
            DEFAULT_FILTER_BY_DATE
        )
        filter_by_date = filter_by.get('date', 'this_month')
        if filter_by_date == 'this_month' and filter_by.get('date_from') is None:
            # first run after login
            today = timezone.now().date()
            first_day = today.replace(day=1)
            last_day = (first_day + datetime.timedelta(days=45)).replace(day=1) - datetime.timedelta(days=1)
            filter_by['date_from'] = first_day.strftime("%Y-%m-%d")
            filter_by['date_to'] = last_day.strftime("%Y-%m-%d")
        if filter_by_date != 'from_the_beginning':
            first_day = datetime.datetime.strptime(filter_by.get('date_from'), "%Y-%m-%d")
            last_day = datetime.datetime.strptime(
                filter_by.get('date_to') or '',
                "%Y-%m-%d"
            ) + datetime.timedelta(days=1)
            first_day = current_timezone.localize(first_day)
            last_day = current_timezone.localize(last_day)
            if first_day:
                queryset = queryset.filter(
                    date__gte=first_day,
                )
            if last_day:
                queryset = queryset.filter(
                    date__lte=last_day
                )
        return queryset


class Transaction(TransactionBase):
    category = models.ForeignKey(
        'TransactionCategory',
        verbose_name=_('Category'),
        blank=True, null=True, default=None,
        on_delete=models.SET_DEFAULT
    )

    objects = FilterByDateManager()

    class Meta:
        ordering = ('-date',)

    def get_short_descr(self):
        if self.title:
            return "{} ({})".format(self.title, self.amount)
        return self.amount

    def __str__(self):
        return '[{}#{}] {} at {}'.format(self.budget.id, self.budget.name, self.amount, self.date)

    def get_json_repr(self):
        fields_to_save = ('id', 'category', 'title', 'amount', 'date')
        result = {}
        for f in fields_to_save:
            result[f] = str(getattr(self, f))
        return result


class IncomeCategory(models.Model):
    # TODO: orderable
    budget = models.ForeignKey('Budget', verbose_name=_('Budget'))
    name = models.CharField(_('Name'), max_length=200)

    def __str__(self):
        return self.name


class Income(TransactionBase):
    category = models.ForeignKey(
        'IncomeCategory',
        verbose_name=_('Income'),
        blank=True, null=True, default=None,
        on_delete=models.SET_DEFAULT
    )

    objects = FilterByDateManager()

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return '[{}#{}] {} at {}'.format(self.budget.id, self.budget.name, self.amount, self.date)
