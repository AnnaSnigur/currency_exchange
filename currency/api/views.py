from rest_framework import generics

from currency.api.serializers import RateSerializer
from currency.models import Rate


class RatesView(generics.ListCreateAPIView):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer
    # queryset = Rate.objects.all()[:20] WRONG

    # useful for 2
    # def get_queryset(self):
    # self.request.user
    #     pass


class RateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer

