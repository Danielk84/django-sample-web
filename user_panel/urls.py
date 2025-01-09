from django.urls import path

from . import views
from blog.models import Event, Entry, EntryImage

app_name = "user_panel"
urlpatterns = [
    path("", views.MainPanelView.as_view(), name="panel"),
    path("login/",views.LoginPanelView.as_view(), name="login"),
    path("logout/", views.logout_panel, name="logout"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("delete_account/", views.delete_account, name="delete_account"),
    path("entries/", views.entry_menu, name="entries"),
    path("events/", views.event_menu, name="events"),
    path("imgs/", views.images_entry_menu, name="imgs"),
    path("edite_entry/<slug:slug>/", views.EntryPanelView.as_view(), name="edite_entry"),
    path("edite_event/<slug:slug>/", views.EventPanelView.as_view(), name="edite_event"),
    path("edite_img/<slug:slug>/", views.ImageEditeView.as_view(), name="edite_image"),
    path("add_entry/", views.EntryPanelView.as_view(), name="add_entry"),
    path("add_event/", views.EventPanelView.as_view(), name="add_event"),
    path("add_img/", views.ImageEditeView.as_view(), name="add_image"),
    path("entry_preview/<slug:slug>/", views.entry_preview, name="entry_preview"),
    path("event_preview/<slug:slug>/", views.event_preview, name="event_preview"),
    path("img_preview/<slug:slug>/", views.img_preview, name="img_preview"),
    path("entry_status/", views.EntryActivationView.as_view(), name="entry_status"),
    path("event_status/", views.EventActivationView.as_view(), name="event_status"),
    path(
        "set_entry_active/<slug:slug>/",
        views.set_status,
        name="set_entry_active",
        kwargs={"obj_class": Entry, "state": True, "rev": "entry"}
    ),
    path(
        "set_event_active/<slug:slug>/",
        views.set_status,
        name="set_event_active",
        kwargs={"obj_class": Event, "state": True, "rev": "event"}
    ),
    path(
        "set_entry_deactive/<slug:slug>/",
        views.set_status,
        name="set_entry_deactive",
        kwargs={"obj_class": Entry, "state": False, "rev": "entry"}
    ),
    path(
        "set_event_deactive/<slug:slug>/",
        views.set_status,
        name="set_event_deactive",
        kwargs={"obj_class": Event, "state": False, "rev": "event"}
    ),
    path(
        "delete_entry/<slug:slug>/",
        views.delete_obj,
        name="delete_entry", 
        kwargs={"model": Entry, "rev": "entries"}
    ),
    path(
        "delete_event/<slug:slug>/",
        views.delete_obj,
        name="delete_event", 
        kwargs={"model": Event, "rev": "events"}
    ),
    path(
        "delete_img/<slug:slug>/",
        views.delete_obj,
        name="delete_img", 
        kwargs={"model": EntryImage, "rev": "imgs"}
    ),
]
