from rest_framework import generics

from account.api.serializers import RateSerializer, ContactSerializer
from account.models import Rate, Contact


class RatesView(generics.ListCreateAPIView):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer


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
