from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse_lazy as rvs
from django.utils.translation import gettext_lazy as _

from .forms import LoginPanelForm


class ValidUserMixin:
    def setUp(self):
        self.username = "testuser"
        self.password = "testpassword"
        self.user = User.objects.create_superuser(
            username=self.username, password=self.password
        )


class LoginPanelViewTestCase(ValidUserMixin, TestCase):
    def setUp(self):
        self.template_name = "user_panel/login.html"
        super().setUp()

    def test_get(self):
        response = self.client.get(rvs("user_panel:login"))
        self.assertTemplateUsed(response, self.template_name)
        self.assertIsInstance(response.context["form"], LoginPanelForm)

    def test_post_valid_data(self):
        data = {"username": self.username, "password": self.password}
        response = self.client.post(rvs("user_panel:login"), data)
        self.assertRedirects(response, rvs("user_panel:panel"))

    def test_post_invalid_user(self):
        data = {"username": "invaliduser", "password": "invalidpassword"}
        response = self.client.post(rvs("user_panel:login"), data)
        self.assertEqual(response.context.get("error"), _("Invalid username or password!"))

    def test_post_invalid_password(self):
        data = {"username": self.username, "password": "invalidpassword"}
        response = self.client.post(rvs("user_panel:login"), data)
        self.assertIsInstance(response.context["form"], LoginPanelForm)

    def test_post_blank_form(self):
        data = {"": self.username, "password": ""}
        response = self.client.post(rvs("user_panel:login"), data)
        self.assertTemplateUsed(response, self.template_name)


class LogoutTestCase(ValidUserMixin, TestCase):
    def setUp(self):
        self.url = rvs("user_panel:logout")
        self.login_url = rvs("user_panel:login")
        super().setUp()

    def test_authenticated(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.url)
        self.assertRedirects(response, self.login_url)

    def test_not_authenticated(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f"{self.login_url}?next={self.url}")