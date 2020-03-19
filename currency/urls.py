from django.urls import path

from currency import views

app_name = 'currency'

urlpatterns = [
    path('rate_list/', views.RateList.as_view(), name='rate_list'),
]
