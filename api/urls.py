from django.urls import path
from .views import register, cancel, get_all_attendees, get_all_events, get_waiting_list

urlpatterns = [
    path("register/", register, name="register"),
    path("cancel/", cancel, name="cancel"),
    path("attendees/", get_all_attendees, name="get_all_attendees"),
    path("events/", get_all_events, name="get_all_events"),
    path("waiting_list/", get_waiting_list, name="get_all_waiting_list"),
]
