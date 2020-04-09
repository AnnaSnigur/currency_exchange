import django_filters
from account.models import Rate
from django.forms import DateInput, DateTimeInput


class RateFilter(django_filters.FilterSet):
    created_date = django_filters.DateFilter(
        field_name='created',
        lookup_expr='date',
        widget=DateInput(
            attrs={
                'class': 'datepicker',
                'type': 'date',
            }
        ))
    # created_dt = django_filters.DateTimeFilter(
    #     field_name='created',
    #     widget=DateTimeInput(
    #         attrs={
    #             'class': 'datetimepicker',
    #             'type': 'datetime',
    #         }
    #     ))

    class Meta:
        model = Rate
        fields = [
            'buy',
            'sale',
            'source',
            'created_date',
            # 'created_dt',
        ]


class FilterRate(django_filters.FilterSet):
    class Meta:
        model = Rate
        fields = {
            'created': ['exact', 'lt', 'lte', 'gt', 'gte', 'range'],
            'currency': ['exact', ],
            'source': ['exact', ],
        }
