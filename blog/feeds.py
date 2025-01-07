from django.contrib.syndication.views import Feed
from django.utils.translation import gettext_lazy as _

from .models import Entry, Event


class WeblogEntryFeed(Feed):
    title = _("The Django weblog")
    link = "http://127.0.0.1:8000/blog/entries/"
    description = _("Latest news on weblog")

    def items(self):
        return Entry.objects.published()[:10]

    def item_pub_date(self, item):
        return item.pub_date

    def item_author_name(self, item):
        return item.author

    def item_description(self, item):
        return item.summary

    def item_link(self, item):
        return item.get_absolute_url()


class WeblogEventFeed(Feed):
    title = _("Our Events")
    link = "http://127.0.0.1:8000/blog/events/"
    description = _("Latest Events on weblog")

    def items(self):
        return Event.objects.published()[:10]

    def item_pub_date(self, item):
        return item.pub_date

    def item_description(self, item):
        return item.detail

    def item_link(self, item):
        return item.get_absolute_url()