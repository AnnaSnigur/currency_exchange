from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from django.conf import settings
from account.tasks import send_email
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView, View, FormView
from account.forms import SignUpForm, ActivateForm
from account.models import User, Contact, ActivationCode, SmsCode


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


class SignUpView(CreateView):
    template_name = 'signup.html'
    queryset = User.objects.all()
    success_url = reverse_lazy('account:activate')
    form_class = SignUpForm

    def get_success_url(self):
        self.request.session['user_id'] = self.object.id
        return super().get_success_url()


class Activate(FormView):
    form_class = ActivateForm
    template_name = 'signup.html'

    def post(self, request):
        user_id = request.session['user_id']
        sms_code = request.POST['sms_code']

        ac = get_object_or_404(
            SmsCode.objects.select_related('user'),
            code=sms_code,
            user_id=user_id,
            is_activated=False,
        )

        if ac.is_expired:
            raise Http404

        ac.is_activated = True
        ac.save(update_fields=['is_activated'])

        user = ac.user
        user.is_active = True
        user.save(update_fields=['is_active'])
        return redirect('index')
