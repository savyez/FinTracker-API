import django_filters
from .models import Transaction

class TransactionFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name='date', lookup_expr='gte') #date format is YYYY-MM-DD
    end_date = django_filters.DateFilter(field_name='date', lookup_expr='lte') #date format is YYYY-MM-DD
    category = django_filters.CharFilter(field_name='category__name', lookup_expr='icontains')
    type = django_filters.CharFilter(field_name='type', lookup_expr='iexact') #type format is 'income' or 'expense'

    class Meta:
        model = Transaction
        fields = ['start_date', 'end_date', 'category', 'type']