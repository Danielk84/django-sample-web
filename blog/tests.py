from datetime import timedelta
from urllib.parse import urlencode
import os
import re

from django.test import TestCase, Client
from django.utils import timezone
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.urls import reverse_lazy as rvs
from django.contrib.sites.models import Site
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import Entry, Event, EntryImage
from .sitemaps import WeblogEntrySitemap ,WeblogEventSitemap


class DateTimeMixin:
    model = None

    def setUp(self):
        self.now = timezone.now()
        self.yesterday = self.now - timedelta(days=1)
        self.tomorrow = self.now + timedelta(days=1)
        self.user = User.objects.create_superuser(username="testUser", password="testPassword")

    def test_is_published(self):
        self.model.objects.create(headline="now", pub_date=self.now, is_active=False, user=self.user)
        self.model.objects.create(headline="tomorrow", pub_date=self.tomorrow, is_active=True, user=self.user)
        self.model.objects.create(headline="yesterday", pub_date=self.yesterday, is_active=True, user=self.user)
        
        self.assertQuerySetEqual(
            self.model.objects.published(),
            ["yesterday"],
            transform=lambda entry: entry.headline,
        )
        self.assertTrue(self.model.objects.get(headline="yesterday").is_published())

    def test_slug_value(self):
        obj = self.model.objects.create(
            headline = "testing slug value",
            pub_date=self.now,
            user=self.user
        )
        slug = slugify(f"{obj.headline}-{obj.pub_date}")

        self.assertEqual(obj.slug, slug)


class EntryTestCase(DateTimeMixin, TestCase):
    model = Entry


class EventTestCase(DateTimeMixin, TestCase):
    model = Event

    def test_past_or_future_event(self):
        Event.objects.create(headline="past", pub_date=self.yesterday, user=self.user)
        Event.objects.create(headline="future", pub_date=self.tomorrow, user=self.user)

        self.assertQuerySetEqual(
            self.model.objects.past(),
            ["past"],
            transform=lambda obj: obj.headline,
        )
        self.assertQuerySetEqual(
            self.model.objects.future(),
            ["future"],
            transform=lambda obj: obj.headline,
        )


class EntryImageTestCase(TestCase):
    model = EntryImage
    file_path = "core/static/favicon.ico"
    
    def setUp(self):
        self.user = User.objects.create_superuser(username="testUser", password="testPassword")
        self.entry = Entry.objects.create(headline="test entry", user=self.user, is_active=True)
        with open(self.file_path, "rb") as file: 
            self.image_file = SimpleUploadedFile(
                name="test_image.ico",
                content=file.read(),
                content_type="image/x-icon"
            )
        self.img = EntryImage.objects.create(
            full_name="test img",
            user=self.user, entry=self.entry,
            place=1,
            image=self.image_file,
        )
    def test_const_fields(self):
        self.assertEqual(self.img.full_name, "test img")
        self.assertEqual(self.img.place, 1)

    def test_slug_value(self):
        self.assertEqual(self.img.slug, slugify(f"{self.img.place}-{self.img.full_name}"))

    def test_get_absolute_url(self):
        self.assertEqual(self.img.get_absolute_url(), rvs(f"weblog:imgs", kwargs={"slug": self.img.slug}))

    def test_image_view(self):
        client = Client(content_type="image/jpeg")
        response = client.get(self.img.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers.get("Content-Type"), "image/jpeg")

    def test_delete_image(self):
        image_path = self.img.image.path
        self.img.delete()
        self.assertFalse(os.path.exists(image_path))

    def tearDown(self):
        if self.img.image and os.path.exists(self.img.image.path):
            os.remove(self.img.image.path)


class SiteMapsTestCase(TestCase):
    def setUp(self):
        date = timezone.now() - timedelta(days=1)
        self.user = User.objects.create_superuser(username="testUser", password="testPassword")
        self.entry = Entry.objects.create(headline="test entry", user=self.user, pub_date=date, is_active=True)
        self.event = Event.objects.create(headline="test event", user=self.user, pub_date=date, is_active=True)

    def test_entry_sitemap(self):
        sitemap = WeblogEntrySitemap()
        urls = sitemap.get_urls(site=Site.objects.get_current())
        self.assertEqual(len(urls), 1)
        self.assertEqual(re.sub(r'https://example\.com', '', urls[0]["location"]), self.entry.get_absolute_url())

    def test_entry_sitemap(self):
        sitemap = WeblogEventSitemap()
        urls = sitemap.get_urls(site=Site.objects.get_current())
        self.assertEqual(len(urls), 1)
        self.assertEqual(re.sub(r'https://example\.com', '', urls[0]["location"]), self.event.get_absolute_url())


class FeedTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username="testUser", password="testPassword")
        self.entry = Entry.objects.create(
            headline="Entry",
            summary="This is the first entry.",
            pub_date=timezone.now() - timedelta(days=2),
            user=self.user,
            is_active=True,
        )
        self.event = Event.objects.create(
            headline="Event",
            detail="This is the first event.",
            pub_date=timezone.now() - timedelta(days=1),
            user=self.user,
            is_active=True,
        )

    def test_weblog_entry_feed(self):
        response = self.client.get(rvs('blog_entry_feed'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.entry.headline)
        self.assertContains(response, self.entry.summary)
        self.assertContains(response, self.entry.user.username)
        self.assertContains(response, self.entry.get_absolute_url())

    def test_weblog_event_feed(self):
        response = self.client.get(rvs('blog_event_feed'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.event.headline)
        self.assertContains(response, self.event.detail)
        self.assertContains(response, self.event.get_absolute_url())


class BaseViewMixin:
    model = None
    obj_count = None
    list_url = ""
    list_template_name = ""
    paginated_by = None
    detail_tempalte_view = ""

    def setUp(self):
        self.user = User.objects.create_superuser(username="testUser", password="testPassword")
        for i in range(self.obj_count):
            self.model.objects.create(
                headline=f"model {i}",
                is_active=True,
                user=self.user,
            )
        self.assertEqual(self.model.objects.count(), self.obj_count)

    def test_list_view(self):
        for i in range(int(self.obj_count / self.paginated_by)):
            response = self.client.get(
                rvs(self.list_url) + "?" + urlencode({"page": i+1})
            )
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, self.list_template_name)
            obj_location = self.obj_count - i * self.paginated_by - 1
            for j in range(obj_location, obj_location-self.paginated_by, -1):
                self.assertContains(response, self.model.objects.get(headline=f"model {j}").headline)

    def test_detail_view(self):
        for obj in self.model.objects.published():
            response = self.client.get(obj.get_absolute_url())
            self.assertTemplateUsed(response, self.detail_tempalte_view)
            self.assertContains(response, obj.headline)


class EntryViewsTestCase(BaseViewMixin, TestCase):
    model = Entry
    obj_count = 100
    list_template_name = "blog/entry_list.html"
    list_url = "weblog:entry_list"
    paginated_by = 10
    detail_tempalte_view = "blog/entry_detail.html"


class EventViewsTestCase(BaseViewMixin, TestCase):
    obj_count = 100
    model = Event
    list_template_name = "blog/event_list.html"
    list_url = "weblog:event_list"
    paginated_by = 10
    detail_tempalte_view = "blog/event_detail.html"