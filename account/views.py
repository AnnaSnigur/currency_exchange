from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from account.models import Contact, User
from django.conf import settings
from account.tasks import send_email
from django.views.generic import UpdateView, CreateView, View


def smoke(request):
    return HttpResponse('smoke')


class MyProfile(UpdateView):
    template_name = 'my_profile.html'
    queryset = User.objects.filter(is_active=True)
    fields = ('email',)
    success_url = reverse_lazy('index')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(id=self.request.user.id)


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


class Contact(CreateView):
    template_name = 'contact.html'
    queryset = Contact.objects.all()
    fields = ('email', 'title', 'text',)
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        title = form.instance.title
        text = form.instance.text
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [form.instance.email, ]
        send_email.delay(title, text, from_email, recipient_list)
        return super().form_valid(form)
