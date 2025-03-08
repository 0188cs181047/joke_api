from django.urls import path
from .views import fetch_jokes, list_jokes

urlpatterns = [
    path('fetch-jokes/', fetch_jokes, name='fetch_jokes'),
    path('list-jokes/', list_jokes, name='list_jokes'),
]