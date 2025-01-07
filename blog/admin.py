from django.contrib import admin

from .models import Entry, Event, EntryImage


@admin.register(Entry, Event)
class SimpleAdmin(admin.ModelAdmin):
    exclude = ["slug"]

admin.site.register(EntryImage)