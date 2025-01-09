from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

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


class RegisterUserForm(forms.ModelForm):
    password = forms.CharField(max_length=32, widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(max_length=32, widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = ["username", "password", "confirm_password", "first_name", "last_name", "email"]
        labels = {
            "username": _("Username"),
            "password": _("Password"),
            "confirm_password": _("Confirm Password"),
            "first_name": _("First Name"),
            "last_name": _("Last Name"),
            "email": _("Email"),
        }
        help_texts = {
            "username": _("Required - 150 characters or fewer - Letters, digits and @/./+/-/_ only."),
            "password": _("Between 8 to 32"),
            "cofirm_password": _("Should be same with password"),
        }

    def clean(self):
        cleaned_data =  super().clean()
        if cleaned_data["password"] == cleaned_data["confirm_password"]:
            return cleaned_data
        raise forms.ValidationError(_("Passwords do not match!"))