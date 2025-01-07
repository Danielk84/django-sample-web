import io

from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Entry, Event, EntryImage

MAX_IMAGES_SIZE = 10 * 1024 * 1024


def image_validator(image):
    try:
        with io.BytesIO() as file:
            image.save(file, image.format)
            if file.seek(0, io.SEEK_END) > MAX_IMAGES_SIZE:
                raise forms.ValidationError(_(f"Image size should not exceed {MAX_IMAGES_SIZE * 1024 * 1024}MB"))
    except:
        forms.ValidationError(_("Invalid Image"))

def image_form_creator(user):
    class ImageForm(forms.ModelForm):
        entry = forms.ModelChoiceField(queryset=Entry.objects.filter(user=user))
        
        class Meta:
            model = EntryImage
            exclude = ["slug", "user"]
            labels = {
                "full_name": _("Image name"),
                "place": _("Place"),
                "image": _("Image"),
                "entry": _("Entry"),
            }
            help_texts = {
                "palce": _("Set palce number for better url"),
                "image": _("Image size should be under - 10MB -"),
            }
            widgets = {
                "image": forms.FileInput
            }
    return ImageForm


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        exclude = ["slug", "is_active", "user"]
        labels = {
            "headline": _("Headline"),
            "pub_date": _("Publication date"),
            "body": _("Body"),
            "summary": _("Summary"),
        }
        help_texts = {
            "headline": _("max length is 200 char"),
            "pub_date": _("set publication date"),
            "summary": _("write summary from you're content for some utilites"),
        }


class EntryActivationForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ["is_active"]


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ["slug", "is_active", "user"]
        labels = {
            "headline": _("Headline"),
            "pub_date": _("Publication date"),
            "location": _("Location"),
            "detail": _("Detail"),
        }
        help_texts = {
            "headline": _("max length is 200 char"),
            "pub_date": _("set publication date"),
        }


class EventActivationForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["is_active"]