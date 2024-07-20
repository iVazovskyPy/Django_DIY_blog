from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class UserRegistrationForm(UserCreationForm):
    bio = forms.CharField(widget=forms.Textarea, max_length=1000)
    phone_number = forms.IntegerField(max_value=99999999999999999999)
    profile_photo = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class CommentForm(forms.Form):
    description = forms.CharField(widget=forms.Textarea, max_length=400)
