from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

#Registration form for new users - styling applied to form fields in this class
class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("username", "password1", "password2")

        labels = {
            "password2": "Confirm Password",   #Custom label
        }

        widgets = {
            "username": forms.TextInput(attrs={"class": "login-form-input"}),
            "password1": forms.PasswordInput(attrs={"class": "login-form-input"}),
            "password2": forms.PasswordInput(attrs={"class": "login-form-input"}),
        }