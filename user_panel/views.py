from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy as rvs
from django.utils.translation import gettext_lazy as _
from django.http import Http404, HttpResponseForbidden

from .forms import LoginPanelForm
from blog.models import Entry, Event, EntryImage
from blog.views import event_detail, entry_detail
from blog.forms import (
    image_form_creator,
    EntryForm,
    EventForm,
)


class LoginPanelView(TemplateView):
    template_name = "user_panel/login.html"

    def get_context_data(self, **kwargs):
        return {"form": LoginPanelForm()}

    def post(self, request):
        form  = LoginPanelForm(request.POST)
        context = {}
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(rvs("user_panel:panel"))
            context["error"] = _("Invalid username or password!")
        context["form"] = form
        return render(request, self.template_name, context)


@login_required
def logout_panel(request):
    logout(request)
    return redirect(rvs("user_panel:login"))


class MainPanelView(LoginRequiredMixin, TemplateView):
    template_name = "user_panel/panel.html"


@login_required
def entry_menu(request):
    entries = Entry.objects.filter(user=request.user)
    return render(request, "user_panel/entry_menu.html", {"entries": entries})


@login_required
def event_menu(request):
    events = Event.objects.filter(user=request.user)
    return render(request, "user_panel/event_menu.html", {"events": events})


@login_required
def entry_preview(request, slug):
    return entry_detail(request, slug, is_draft=True)


@login_required
def event_preview(request, slug):
    return event_detail(request, slug, is_draft=True)


class PanelViewMixin:
    template_name = None
    form_class = None
    model = None
    redirect_link = None

    def get_initial(self, obj) -> dict:
        return {}

    def get(self, request, slug=None):
        form = None
        context = {}
        if slug is not None:
            obj = get_object_or_404(self.model, slug=slug, user=request.user)
            form = self.form_class(initial=self.get_initial(obj))
            context["obj"] = obj
        context["form"] = form or self.form_class()
        return render(request, self.template_name, context)

    def post(self, request, slug=None):
        context = {}
        if slug is not None:
            obj = get_object_or_404(self.model, slug=slug, user=request.user)
            form = self.form_class(request.POST, instance=obj)
            if form.is_valid():
                obj.save()
            context["obj"] = obj
        else:
            obj = self.model()
            form = self.form_class(request.POST, instance=obj)
            if form.is_valid():
                obj.user = request.user
                obj.save()
                return redirect(self.redirect_link)
            
        context["form"] = form
        return render(request, self.template_name, context)


class EntryPanelView(LoginRequiredMixin, PanelViewMixin, View):
    template_name = "user_panel/entry_panel.html"
    form_class = EntryForm
    model = Entry
    redirect_link = "user_panel:entries"

    def get_initial(self, obj):
        return {
            "headline": obj.headline,
            "pub_date": obj.pub_date,
            "body": obj.body,
            "summary": obj.summary,
        }


class EventPanelView(LoginRequiredMixin, PanelViewMixin, View):
    template_name = "user_panel/event_panel.html"
    form_class = EventForm
    model = Event
    redirect_link = "user_panel:events"

    def get_initial(self, obj):
        return {
            "headline": obj.headline,
            "pub_date": obj.pub_date,
            "location": obj.location,
            "detail": obj.detail,
        }


@login_required
def images_entry_menu(request):
    imgs = EntryImage.objects.filter(user=request.user)
    return render(request, "user_panel/image_panel.html", {"imgs": imgs})


class ImageEditeView(LoginRequiredMixin, View):
    template_name = "user_panel/image_edite_page.html"

    def get(self, request, slug=None):
        form = None
        context = {}
        if slug is not None:
            img = get_object_or_404(EntryImage, slug=slug)
            if img.user.username != request.user.username:
                raise Http404()
            form = image_form_creator(request.user)(
                initial={
                    "full_name": img.full_name,
                    "place": img.place,
                    "image": img.image,
                    "entry": img.entry
                }
            )
            context["img"] = img
        context["form"] = form or image_form_creator(request.user)()
        return render(request, self.template_name, context)

    def post(self, request, slug=None):
        context = {}
        if slug is not None:
            img = get_object_or_404(EntryImage, slug=slug)
            form = image_form_creator(request.user)(request.POST, request.FILES, instance=img)
            if form.is_valid():
                img.save()
            context["img"] = img
        else:
            img = EntryImage()
            form = image_form_creator(request.user)(request.POST, request.FILES, instance=img)
            if form.is_valid():
                img.user = request.user
                img.save()
                return redirect("user_panel:imgs")

        context["form"] = form
        return render(request, self.template_name, context)


class ActivationMixin:
    template_name = None
    model = None

    def get(self, request):
        if request.user.is_superuser:
            objs = self.model.objects.order_by("is_active")
            return render(request, self.template_name, {"objs": objs})
        return HttpResponseForbidden()


class EntryActivationView(LoginRequiredMixin, ActivationMixin, View):
    template_name = "user_panel/entry_activation.html"
    model = Entry


class EventActivationView(LoginRequiredMixin, ActivationMixin, View):
    template_name = "user_panel/event_activation.html"
    model = Event


@login_required
def set_active(request, slug, obj_class, state, rev):
    obj = get_object_or_404(obj_class, slug=slug)
    if request.user.is_superuser:
        if hasattr(obj, "is_active"):
            obj.is_active = state
            obj.save()
            return redirect(f"user_panel:{rev}_status")
        raise Http404()
    return HttpResponseForbidden()