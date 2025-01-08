from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.i18n import i18n_patterns
from django.contrib.sitemaps.views import sitemap
from django.conf import settings 
from django.views.static import serve

from blog.views import image
from blog.feeds import WeblogEventFeed, WeblogEntryFeed
from blog.sitemaps import WeblogEntrySitemap, WeblogEventSitemap

sitemaps = {
    "weblog_entry": WeblogEntrySitemap,
    "weblog_event": WeblogEventSitemap,
}
urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}),
]
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path("home/", include("home.urls")),
    path("blog/", include("blog.urls")),
    path("panel/", include("user_panel.urls")),
    path("rss/blog/entry/", WeblogEntryFeed(), name="blog_entry_feed"),
    path("rss/blog/event/", WeblogEventFeed(), name="blog_event_feed"),
)
if settings.DEBUG:
    urlpatterns += [
        path("static/<path:path>/", serve, {"document_root":settings.STATIC_ROOT}),
        path("media/<path:path>/", serve, {"document_root": settings.MEDIA_ROOT}),
    ]