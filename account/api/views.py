from rest_framework import generics
from account.api.serializers import RateSerializer, ContactSerializer
from account.models import Rate, Contact
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from account.models import Rate
from account.api.filter import RateFilter
from account.api.serializers import RateSerializer


class RatesView(generics.ListCreateAPIView):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer
    filterset_class = RateFilter
    pagination_class = PageNumberPagination


class RateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer


class ContactsView(generics.ListCreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def get_queryset(self):
        user = self.request.user
        return super().get_queryset().filter(email=user.email)


class ContactView(generics.RetrieveUpdateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

