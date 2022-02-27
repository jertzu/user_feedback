from django import forms

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Feedback

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ["body"]