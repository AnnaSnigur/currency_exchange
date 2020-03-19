from django.views.generic import ListView

from .models import Rate


class RateList(ListView):
    model = Rate
    paginate_by = 5
    queryset = Rate.objects.all()[:20]