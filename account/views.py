from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView
from account.models import Contact


def smoke(request):
    return HttpResponse('smoke')


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


class Contact(CreateView):
    template_name = 'base.html'
    queryset = Contact.objects.all()
    fields = ('email', 'title', 'text', )
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        response = super().form_invalid(form)
        return response
