from django.contrib.sitemaps import Sitemap

from .models import Entry, Event


class WeblogEntrySitemap(Sitemap):
    changefreq = "weakly"
    priority = 0.7

    def items(self):
        return Entry.objects.published()


class WeblogEventSitemap(Sitemap):
    changefreq = "weakly"
    priority = 0.7

    def items(self):
        return Event.objects.published()