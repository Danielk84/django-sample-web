from django.urls import path

from . import views
from blog.models import Event, Entry

app_name = "user_panel"
urlpatterns = [
    path("", views.MainPanelView.as_view(), name="panel"),
    path("login/",views.LoginPanelView.as_view(), name="login"),
    path("logout/", views.logout_panel, name="logout"),
    path("entries/", views.entry_menu, name="entries"),
    path("entry_preview/<slug:slug>/", views.entry_preview, name="entry_preview"),
    path("edite_entry/<slug:slug>/", views.EntryPanelView.as_view(), name="edite_entry"),
    path("add_entry/", views.EntryPanelView.as_view(), name="add_entry"),
    path("imgs/", views.images_entry_menu, name="imgs"),
    path("add_img/", views.ImageEditeView.as_view(), name="add_image"),
    path("edite_img/<slug:slug>/", views.ImageEditeView.as_view(), name="edite_image"),
    path("events/", views.event_menu, name="events"),
    path("edite_event/<slug:slug>/", views.EventPanelView.as_view(), name="edite_event"),
    path("edite_event/", views.EventPanelView.as_view(), name="add_event"),
    path("event_preview/<slug:slug>/", views.event_preview, name="event_preview"),
    path("entry_status/", views.EntryActivationView.as_view(), name="entry_status"),
    path("event_status/", views.EventActivationView.as_view(), name="event_status"),
    path(
        "set_entry_active/<slug:slug>/",
        views.set_active,
        name="set_entry_active",
        kwargs={"obj_class": Entry, "state": True, "rev": "entry"}
    ),
    path(
        "set_event_active/<slug:slug>/",
        views.set_active,
        name="set_event_active",
        kwargs={"obj_class": Event, "state": True, "rev": "event"}
    ),
    path(
        "set_entry_deactive/<slug:slug>/",
        views.set_active,
        name="set_entry_deactive",
        kwargs={"obj_class": Entry, "state": False, "rev": "entry"}
    ),
    path(
        "set_event_deactive/<slug:slug>/",
        views.set_active,
        name="set_event_deactive",
        kwargs={"obj_class": Event, "state": False, "rev": "event"}
    ),
]
