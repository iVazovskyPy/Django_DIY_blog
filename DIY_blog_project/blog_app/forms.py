from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm

from .models import Blog


class UserRegistrationForm(UserCreationForm):
    bio = forms.CharField(widget=forms.Textarea, max_length=1000)
    phone_number = forms.IntegerField(max_value=99999999999999999999)
    profile_photo = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class CommentForm(forms.Form):
    description = forms.CharField(widget=forms.Textarea, max_length=400)


class ProfileEditForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    profile_photo = forms.ImageField(required=False)
    phone_number = forms.IntegerField()
    bio = forms.CharField(widget=forms.Textarea, max_length=1000)


class BlogEditForm(ModelForm):
    class Meta:
        model = Blog
        fields = ['name', 'content']
