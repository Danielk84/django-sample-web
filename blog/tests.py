from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from django.template.defaultfilters import slugify

from .models import Entry, Event


class DateTimeMixin:
    model = None

    def setUp(self):
        self.now = timezone.now()
        self.yesterday = self.now - timedelta(days=1)
        self.tomorrow = self.now + timedelta(days=1)

    def test_is_published(self):
        self.model.objects.create(headline="now", pub_date=self.now, is_active=False)
        self.model.objects.create(headline="tomorrow", pub_date=self.tomorrow, is_active=True)
        self.model.objects.create(headline="yesterday", pub_date=self.yesterday, is_active=True)
        
        self.assertQuerySetEqual(
            self.model.objects.published(),
            ["yesterday"],
            transform=lambda entry: entry.headline,
        )
        self.assertTrue(self.model.objects.get(headline="yesterday").is_published())

    def test_slug_value(self):
        entry = self.model.objects.create(
            headline = "testing slug value",
            pub_date=self.now,
        )
        slug = slugify(f"{entry.headline}-{entry.pub_date}")

        self.assertEqual(entry.slug, slug)


class EntryTestCase(DateTimeMixin, TestCase):
    model = Entry


class EventTestCase(DateTimeMixin, TestCase):
    model = Event

    def test_past_or_future_event(self):
        Event.objects.create(headline="past", pub_date=self.yesterday)
        Event.objects.create(headline="future", pub_date=self.tomorrow)

        self.assertQuerySetEqual(
            self.model.objects.past(),
            ["past"],
            transform=lambda entry: entry.headline,
        )
        self.assertQuerySetEqual(
            self.model.objects.future(),
            ["future"],
            transform=lambda entry: entry.headline,
        )