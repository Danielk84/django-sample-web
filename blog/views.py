from django.views.generic import ListView
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, render

from .models import Entry, Event, EntryImage


class EntryList(ListView):
    model = Entry
    template_name = "blog/entry_list.html"

    def get_context_data(self, **kwargs):
        return {"object_list": self.model.objects.published()}


def entry_detail(request, slug, is_draft=False):
    entry = get_object_or_404(Entry, slug=slug)
    if not is_draft and not entry.is_published():
        raise Http404()
    return render(
        request,
        "blog/entry_detail.html",
        {"object": entry},
    )


class EventList(ListView):
    model = Event
    template_name = "blog/event_list.html"

    def get_context_data(self, **kwargs):
        return {"object_list": self.model.objects.published()}



def event_detail(request, slug, is_draft=False):
    event = get_object_or_404(Event, slug=slug)
    if not is_draft and not event.is_published():
        raise Http404()
    return render(
        request,
        "blog/event_detail.html",
        {"object": event},
    )


def image(request, slug, is_draft=False):
    img = get_object_or_404(EntryImage, slug=slug)
    if not is_draft and not img.entry.is_published():    
        raise Http404()
    return HttpResponse(
        img.image,
        content_type = "image/jpeg"
    )