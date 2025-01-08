from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.urls import reverse_lazy as rvs


class EntryQuerySet(models.QuerySet):
    def published(self):
        return self.active().filter(pub_date__lte=timezone.now())

    def active(self):
        return self.filter(is_active=True)


class Entry(models.Model):
    headline = models.CharField(max_length=200)
    slug = models.SlugField(allow_unicode=True, unique=True, )
    is_active = models.BooleanField(
        default=False,
        help_text=_("Tick to make this entry live, if it's good and approved"),
    )
    pub_date = models.DateTimeField(
        verbose_name=_("Publication date"),
        help_text=_("Date of Publication"),
        default=timezone.now,
    )
    body = models.TextField()
    summary = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    objects = EntryQuerySet.as_manager()

    class Meta:
        verbose_name_plural = "entries"
        ordering = ["-pub_date"]
        get_latest_by = "pub_date"

    def get_absolute_url(self):
        return rvs("weblog:entry_detail", kwargs={"slug": self.slug })
    
    def __str__(self):
        return self.headline
    
    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.headline}-{self.pub_date}")
        super().save(*args, **kwargs)

    def is_published(self):
        return self.is_active and self.pub_date <= timezone.now()


class EventQuerySet(EntryQuerySet):
    def past(self):
        return self.filter(pub_date__lte=timezone.now())

    def future(self):
        return self.filter(pub_date__gte=timezone.now())


class Event(models.Model):
    headline = models.CharField(max_length=200)
    slug = models.SlugField(allow_unicode=True, unique=True, )
    is_active = models.BooleanField(
        default=False,
        help_text=_("Tick to make this event live, if it's good and approved"),
    )
    pub_date = models.DateTimeField(
        verbose_name=_("Publication date"),
        help_text=_("Date of Publication"),
        default=timezone.now,
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(
        max_length=400,
        help_text=_("location or address of event")
    )
    detail = models.TextField(blank=True)

    objects = EventQuerySet.as_manager()

    class Meta:
        verbose_name_plural = "events"
        ordering = ["-pub_date"]
        get_latest_by = "pub_date"
        indexes = [
            models.Index(fields=["headline", "slug", "is_active", "pub_date"])
        ]

    def get_absolute_url(self):
        return rvs("weblog:event_detail", kwargs={"slug": self.slug })

    def __str__(self):
        return self.headline

    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.headline}-{self.pub_date}")
        super().save(*args, **kwargs)

    def is_published(self):
        return self.is_active and self.pub_date <= timezone.now()


class EntryImage(models.Model):
    full_name = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(unique=True)
    place = models.PositiveIntegerField(default=1)
    image = models.ImageField(upload_to="entry_media/")
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ["entry", "place"]    

    def get_absolute_url(self):
        return rvs(f"/img/blog/{self.slug}/")

    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.place}-{self.full_name}")
        super().save(*args, **kwargs)

    def delete(self, using = None, keep_parents = False):
        self.image.delete(False)
        super().delete(using, keep_parents)

    def __str__(self):
        return self.full_name