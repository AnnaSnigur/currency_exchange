from django.urls import path, include
from django.contrib import admin
from account import views

app_name = 'account'

urlpatterns = [
    path('smoke/', views.smoke, name='smoke'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('contact/', views.Contact.as_view(), name='contact'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('activate/', views.Activate.as_view(), name='activate'),
    path('index/', views.Index.as_view(), name='index'),
]

