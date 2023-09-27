from io import DEFAULT_BUFFER_SIZE
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('result', views.result, name='viewresult'),
]