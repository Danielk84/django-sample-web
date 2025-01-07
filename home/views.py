from django.views.generic import TemplateView

from blog.models import Entry, Event


class IndexPageView(TemplateView):
    template_name = "home/index.html"

    def get_context_data(self, **kwargs):
        context = {
            "lastest_entries": Entry.objects.published()[:3],
            "lastest_events": Event.objects.published()[:3],
        }
        return context
