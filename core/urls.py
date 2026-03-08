from django.urls import path
from .views import EventCreateView


urlpatterns = [path('events/', EventCreateView.as_view(), name='events-create')]

