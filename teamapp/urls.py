from io import DEFAULT_BUFFER_SIZE
from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_db, name='search_db'),
    path('result', views.result, name='viewresult'),
    path('home/', views.home, name='home'),
    path('new/', views.new, name='new'),
    
    
]