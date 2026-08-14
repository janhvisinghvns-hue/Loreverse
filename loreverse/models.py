from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to="profile_pictures/", blank=True)

class Story(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Chapter(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name="chapters")
    title = models.CharField(max_length=200)
    content = models.TextField()
    chapter_number = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.story.title} - Chapter {self.chapter_number}"    

        