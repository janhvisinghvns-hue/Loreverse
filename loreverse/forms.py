from django import forms
from .models import Profile , Story , Chapter
from django.contrib.auth.forms import PasswordChangeForm


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["bio" , "profile_picture"]

class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ["title", "genre", "tags", "description"]

class ChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = ["chapter_number", "title", "content"]        