from django.urls import path
from . import views
from . import sms

urlpatterns = [
    path('', views.index, name='index'),
    path('sms', sms.callback, name='index'),
]
