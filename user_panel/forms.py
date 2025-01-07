from django import forms
from django.utils.translation import gettext_lazy as _


class LoginPanelForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        help_text=_("Enter you're username"),
    )
    password = forms.CharField(
        max_length=32,
        help_text=_("Enter you're password"),
        widget=forms.PasswordInput,
    )