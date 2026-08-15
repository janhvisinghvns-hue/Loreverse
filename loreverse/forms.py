from django import forms
from .models import (Profile , Story , Chapter , Character ,Location,Creature,TimelineEvent,WorldImage,
    CharacterImage,
    LocationImage,
    CreatureImage , ChapterComment)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["bio" , "profile_picture"]

class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ["title", "genre", "tags", "description" , "cover_image"]

class ChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = ["chapter_number", "title", "content"]        

class CharacterForm(forms.ModelForm):
    class Meta:
        model = Character
        fields = ["name"]        

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ["name"]  

class CreatureForm(forms.ModelForm):
    class Meta:
        model = Creature
        fields = ["name"]

class TimelineEventForm(forms.ModelForm):
    class Meta:
        model = TimelineEvent
        fields = ["date", "title", "description"]  

class WorldImageForm(forms.ModelForm):
    class Meta:
        model = WorldImage
        fields = ["image"]


class CharacterImageForm(forms.ModelForm):
    class Meta:
        model = CharacterImage
        fields = ["image"]


class LocationImageForm(forms.ModelForm):
    class Meta:
        model = LocationImage
        fields = ["image"]


class CreatureImageForm(forms.ModelForm):
    class Meta:
        model = CreatureImage
        fields = ["image"]              

class ChapterCommentForm(forms.ModelForm):
    class Meta:
        model = ChapterComment
        fields = ["content"]
        labels = {
            "content": "Comment"
        }
        widgets = {
            "content": forms.Textarea(attrs={
                "rows": 3,
                "placeholder": "Write a comment..."
            })
        }
              

