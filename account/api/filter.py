import django_filters
from account.models import Rate


class FilterRate(django_filters.FilterSet):
    class Meta:
        model = Rate
        fields = {
            'created': ['exact', 'lt', 'lte', 'gt', 'gte', 'range'],
            'currency': ['exact', ],
            'source': ['exact', ],
        }
