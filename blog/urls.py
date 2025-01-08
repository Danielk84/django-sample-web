from django.urls import path

from . import views

app_name = "weblog"
urlpatterns = [
    path("entries/", views.EntryList.as_view(), name="entry_list"),
    path("entry/<slug:slug>/", views.entry_detail, name="entry_detail"),
    path("events/", views.EventList.as_view(), name="event_list"),
    path("event/<slug:slug>/", views.event_detail, name="event_detail"),
    path("imgs/<slug:slug>/", views.image, name="imgs"),
]