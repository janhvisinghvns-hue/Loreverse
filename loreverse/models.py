from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to="profile_pictures/", blank=True)

class Story(models.Model):
    GENRE_CHOICES = [
        ("Fantasy", "Fantasy"),
        ("Romance", "Romance"),
        ("Mystery", "Mystery"),
        ("Horror", "Horror"),
        ("Science Fiction", "Science Fiction"),
        ("Adventure", "Adventure"),
        ("Other", "Other"),]
    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=30, choices=GENRE_CHOICES, default="Other")
    tags = models.CharField(max_length=300, blank=True)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    favorited_by = models.ManyToManyField(User, related_name="favorite_stories", blank=True)
    want_to_read_by = models.ManyToManyField(User, related_name="want_to_read_stories", blank=True)
    

    def __str__(self):
        return self.title

class World(models.Model):
    story = models.OneToOneField(
        Story,
        on_delete=models.CASCADE,
        related_name="world"
    )
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.story.title} World"


class WorldImage(models.Model):
    world = models.ForeignKey(
        World,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(upload_to="world_images/")

    def __str__(self):
        return f"{self.world.story.title} World Image"


class Character(models.Model):
    world = models.ForeignKey(
        World,
        on_delete=models.CASCADE,
        related_name="characters"
    )
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class CharacterImage(models.Model):
    character = models.ForeignKey(
        Character,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(upload_to="character_images/")

    def __str__(self):
        return f"{self.character.name} Image"


class Location(models.Model):
    world = models.ForeignKey(
        World,
        on_delete=models.CASCADE,
        related_name="locations"
    )
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class LocationImage(models.Model):
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(upload_to="location_images/")

    def __str__(self):
        return f"{self.location.name} Image"


class Creature(models.Model):
    world = models.ForeignKey(
        World,
        on_delete=models.CASCADE,
        related_name="creatures"
    )
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class CreatureImage(models.Model):
    creature = models.ForeignKey(
        Creature,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(upload_to="creature_images/")

    def __str__(self):
        return f"{self.creature.name} Image"


class TimelineEvent(models.Model):
    world = models.ForeignKey(
        World,
        on_delete=models.CASCADE,
        related_name="timeline"
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date = models.CharField(max_length=100)

    def __str__(self):
        return self.title                    

class Chapter(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name="chapters")
    title = models.CharField(max_length=200)
    content = models.TextField()
    chapter_number = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.story.title} - Chapter {self.chapter_number}"    

class ReadingProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "story")

    def __str__(self):
        return f"{self.user.username} - {self.story.title}"       

class ReadingHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    last_read_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "story")

    def __str__(self):
        return f"{self.user.username} - {self.story.title}"

class CompletedStory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "story")

    def __str__(self):
        return f"{self.user.username} - {self.story.title}"        