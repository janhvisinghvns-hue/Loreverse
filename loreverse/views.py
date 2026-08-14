from django.shortcuts import render , redirect ,  get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login , authenticate , logout
from django.db import IntegrityError
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from .models import (Profile, Story, Chapter, ReadingProgress, ReadingHistory, 
    CompletedStory, World, Character, Location, Creature,TimelineEvent,WorldImage, CharacterImage,
    LocationImage,CreatureImage, ChapterLike, ChapterComment)
from .forms import( ProfileForm , StoryForm , ChapterForm, CharacterForm,LocationForm, CreatureForm,
    TimelineEventForm, CreatureImageForm,LocationImageForm,CharacterImageForm,WorldImageForm, ChapterCommentForm)
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.db.models import Q


def index(request):
    progress = None

    if request.user.is_authenticated:
        progress = ReadingProgress.objects.filter(
            user=request.user
        ).select_related("story", "chapter").first()

    fantasy_stories = Story.objects.filter(published=True, genre="Fantasy")[:5]

    mystery_stories = Story.objects.filter(published=True,genre="Mystery")[:5]

    adventure_stories = Story.objects.filter(published=True,genre="Adventure")[:5]

    return render(request, "loreverse/index.html", {
        "progress": progress,
        "fantasy_stories": fantasy_stories,
        "mystery_stories": mystery_stories,
        "adventure_stories": adventure_stories,
    })


def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        username = username.strip()
        email = email.strip()
        if not username or not email or not password or not confirmation:
           return render(request, "loreverse/register.html", {
              "message": "All fields are required."
            })
        if password != confirmation:
            return render(request, "loreverse/register.html", {
                "message": "Passwords must match."
            })
        try:
          user = User.objects.create_user(username, email, password)
          user.save()
          Profile.objects.create(user=user, role="Reader")
        except IntegrityError:
            return render(request, "loreverse/register.html", {
                "message": "Username already taken."
            })    
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "loreverse/register.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        username = username.strip()
        if not username or not password:
            return render(request, "loreverse/login.html", {
             "message": "Username and password are required."
            })
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "loreverse/login.html", {
                "message": "Invalid username and/or password."
            })

    else:
        return render(request, "loreverse/login.html")  

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

@login_required
def profile_view(request):
    profile = request.user.profile

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("profile"))

    else:
        form = ProfileForm(instance=profile)

    return render(request, "loreverse/profile.html", {
        "profile": profile,
        "form": form
    })

@login_required
def become_writer(request):
    profile = request.user.profile

    if request.method == "POST":
        profile.role = "Writer"
        profile.save()
        return redirect("profile")
    return render(request, "loreverse/become_writer.html")

def change_password_view(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return HttpResponseRedirect(reverse("profile"))

    else:
        form = PasswordChangeForm(request.user)

    return render(request, "loreverse/change_password.html", {
        "form": form
    })


@login_required
def create_story(request):
    if request.user.profile.role != "Writer":
        return redirect("profile")

    if request.method == "POST":
        form = StoryForm(request.POST)

        if form.is_valid():
            story = form.save(commit=False)
            story.author = request.user
            story.save()
            return redirect("index")
    else:
        form = StoryForm()
    return render(request, "loreverse/create_story.html", {"form": form})


@login_required
def my_stories(request):
    stories = Story.objects.filter(author=request.user)
    return render(request, "loreverse/my_stories.html", {"stories": stories})

@login_required
def create_world(request, story_id):
    story = get_object_or_404(Story, id=story_id, author=request.user)

    if request.user.profile.role != "Writer":
        return redirect("profile")

    if hasattr(story, "world"):
        return redirect("world_explorer", story_id=story.id)

    if request.method == "POST":
        description = request.POST.get("description", "").strip()

        World.objects.create(
            story=story,
            description=description
        )

        return redirect("world_explorer", story_id=story.id)

    return render(request, "loreverse/create_world.html", {
        "story": story
    })

@login_required
def world_explorer(request, story_id):
    story = get_object_or_404(Story, id=story_id)

    if not story.published and story.author != request.user:
        return redirect("index")

    world = get_object_or_404(World, story=story)

    return render(request, "loreverse/world_explorer.html", {
        "story": story, "world": world,
    })


@login_required
def create_character(request, story_id):
    story = get_object_or_404(Story, id=story_id, author=request.user)

    if request.user.profile.role != "Writer":
        return redirect("profile")

    world = get_object_or_404(World, story=story)

    if request.method == "POST":
        form = CharacterForm(request.POST)

        if form.is_valid():
            character = form.save(commit=False)
            character.world = world
            character.save()
            return redirect("world_explorer", story_id=story.id)
    else:
        form = CharacterForm()

    return render(request, "loreverse/create_character.html", {
        "form": form,
        "story": story,
    })

@login_required
def create_location(request, story_id):
    story = get_object_or_404(Story, id=story_id, author=request.user)

    if request.user.profile.role != "Writer":
        return redirect("profile")

    world = get_object_or_404(World, story=story)

    if request.method == "POST":
        form = LocationForm(request.POST)

        if form.is_valid():
            location = form.save(commit=False)
            location.world = world
            location.save()
            return redirect("world_explorer", story_id=story.id)
    else:
        form = LocationForm()

    return render(request, "loreverse/create_location.html", {
        "form": form,
        "story": story,
    })

@login_required
def create_creature(request, story_id):
    story = get_object_or_404(Story, id=story_id, author=request.user)

    if request.user.profile.role != "Writer":
        return redirect("profile")

    world = get_object_or_404(World, story=story)

    if request.method == "POST":
        form = CreatureForm(request.POST)

        if form.is_valid():
            creature = form.save(commit=False)
            creature.world = world
            creature.save()
            return redirect("world_explorer", story_id=story.id)
    else:
        form = CreatureForm()

    return render(request, "loreverse/create_creature.html", {
        "form": form,
        "story": story,
    })

@login_required
def create_timeline_event(request, story_id):
    story = get_object_or_404(Story, id=story_id, author=request.user)

    if request.user.profile.role != "Writer":
        return redirect("profile")

    world = get_object_or_404(World, story=story)

    if request.method == "POST":
        form = TimelineEventForm(request.POST)

        if form.is_valid():
            event = form.save(commit=False)
            event.world = world
            event.save()
            return redirect("world_explorer", story_id=story.id)
    else:
        form = TimelineEventForm()

    return render(request, "loreverse/create_timeline_event.html", {
        "form": form,
        "story": story,
    })

@login_required
def edit_story(request, story_id):
    story = get_object_or_404(Story, id=story_id, author=request.user)

    if request.user.profile.role != "Writer":
        return redirect("profile")

    if request.method == "POST":
        form = StoryForm(request.POST, instance=story)

        if form.is_valid():
            form.save()
            return redirect("my_stories")
    else:
        form = StoryForm(instance=story)

    return render(request, "loreverse/edit_story.html", {
        "form": form, "story": story
    })

@login_required
def delete_story(request, story_id):
    story = get_object_or_404(Story, id=story_id, author=request.user)
    if request.user.profile.role != "Writer":
        return redirect("profile")

    if request.method == "POST":
        story.delete()
        return redirect("my_stories")
    return render(request, "loreverse/delete_story.html", {
        "story": story
    })

@login_required
def publish_story(request, story_id):
    story = get_object_or_404(Story, id=story_id, author=request.user)
    if request.user.profile.role != "Writer":
        return redirect("profile")
    if request.method == "POST":
        story.published = True
        story.save()
    return redirect("my_stories")

def published_stories(request):
    query = request.GET.get("q", "").strip()
    genre = request.GET.get("genre", "").strip()
    tag = request.GET.get("tag", "").strip()
    sort = request.GET.get("sort", "").strip()
    stories = Story.objects.filter(published=True)
    if query:
        stories = stories.filter(
            Q(title__icontains=query) |
            Q(author__username__icontains=query)
        )
    if genre:
        stories = stories.filter(genre=genre)

    if tag:
        stories = stories.filter(tags__icontains=tag)    

    if sort == "newest":
        stories = stories.order_by("-created_at")  
    elif sort == "oldest":
         stories = stories.order_by("created_at")    

    return render(request, "loreverse/published_stories.html", {
        "stories": stories, "query": query, "genre": genre, 
        "tag": tag, "sort": sort, "genre_choices": Story.GENRE_CHOICES,
    })

def story_detail(request, story_id):
    story = get_object_or_404(Story, id=story_id, published=True)
    chapters = story.chapters.all().order_by("chapter_number")
    completed = False

    if request.user.is_authenticated:
        completed = CompletedStory.objects.filter(
            user=request.user,
            story=story
        ).exists()
    return render(request, "loreverse/story_detail.html", {"story": story, "chapters": chapters , "completed": completed})

@login_required
def toggle_favorite(request, story_id):
    story = get_object_or_404(Story, id=story_id, published=True)
    if request.user in story.favorited_by.all():
        story.favorited_by.remove(request.user)
    else:
        story.favorited_by.add(request.user)
    return redirect("story_detail", story_id=story.id)

@login_required
def toggle_want_to_read(request, story_id):
    story = get_object_or_404(Story, id=story_id, published=True)

    if request.user in story.want_to_read_by.all():
        story.want_to_read_by.remove(request.user)
    else:
        story.want_to_read_by.add(request.user)
    return redirect("story_detail", story_id=story.id)

@login_required
def toggle_completed(request, story_id):
    story = get_object_or_404(Story, id=story_id, published=True)

    completed = CompletedStory.objects.filter(user=request.user, story=story).first()

    if completed:
        completed.delete()
    else:
        CompletedStory.objects.create(user=request.user, story=story)

    return redirect("story_detail", story_id=story.id)

@login_required
def create_chapter(request, story_id):
    story = get_object_or_404(Story, id=story_id, author=request.user)

    if request.user.profile.role != "Writer":
        return redirect("profile")

    if request.method == "POST":
        form = ChapterForm(request.POST)

        if form.is_valid():
            chapter = form.save(commit=False)
            chapter.story = story
            chapter.save()
            return redirect("story_detail", story_id=story.id)
    else:
        form = ChapterForm()
    return render(request, "loreverse/create_chapter.html", {
        "form": form, "story": story})

@login_required
def read_chapter(request, story_id, chapter_id):
    story = get_object_or_404(Story, id=story_id, published=True)
    chapter = get_object_or_404(
        Chapter,
        id=chapter_id,
        story=story
    )

    chapters = list(
        story.chapters.all().order_by("chapter_number")
    )

    current_index = chapters.index(chapter)

    previous_chapter = None
    next_chapter = None

    if current_index > 0:
        previous_chapter = chapters[current_index - 1]

    if current_index < len(chapters) - 1:
        next_chapter = chapters[current_index + 1]

    ReadingProgress.objects.update_or_create(
        user=request.user,
        story=story,
        defaults={"chapter": chapter}
    )

    ReadingHistory.objects.update_or_create(
        user=request.user,
        story=story
    )

    if request.method == "POST":
        comment_form = ChapterCommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.chapter = chapter
            comment.save()

            return redirect(
                "read_chapter",
                story_id=story.id,
                chapter_id=chapter.id
            )
    else:
        comment_form = ChapterCommentForm()

    likes_count = chapter.likes.count()

    user_liked = ChapterLike.objects.filter(
        user=request.user,
        chapter=chapter
    ).exists()

    comments = chapter.comments.all().order_by("created_at")

    return render(request, "loreverse/read_chapter.html", {
        "story": story,
        "chapter": chapter,
        "previous_chapter": previous_chapter,
        "next_chapter": next_chapter,
        "likes_count": likes_count,
        "user_liked": user_liked,
        "comment_form": comment_form,
        "comments": comments,
    })

@login_required
def continue_reading(request, story_id):
    progress = get_object_or_404(ReadingProgress, user=request.user, story_id=story_id)

    return redirect("read_chapter", story_id=progress.story.id, chapter_id=progress.chapter.id)


@login_required
def reader_dashboard(request):
    progress = ReadingProgress.objects.filter(
        user=request.user
    ).select_related("story", "chapter")

    favorites = request.user.favorite_stories.all()

    want_to_read = request.user.want_to_read_stories.all()

    completed_stories = CompletedStory.objects.filter(
        user=request.user
    ).select_related("story")

    reading_history = ReadingHistory.objects.filter(
        user=request.user
    ).select_related("story").order_by("-last_read_at")

    return render(request, "loreverse/reader_dashboard.html", {
        "progress": progress,
        "favorites": favorites,
        "want_to_read": want_to_read,
        "completed_stories": completed_stories,
        "reading_history": reading_history,
    })

@login_required
def add_world_image(request, story_id):
    story = get_object_or_404(Story, id=story_id, author=request.user)

    if request.user.profile.role != "Writer":
        return redirect("profile")

    world = get_object_or_404(World, story=story)

    if request.method == "POST":
        form = WorldImageForm(request.POST, request.FILES)

        if form.is_valid():
            world_image = form.save(commit=False)
            world_image.world = world
            world_image.save()
            return redirect("world_explorer", story_id=story.id)
    else:
        form = WorldImageForm()

    return render(request, "loreverse/add_world_image.html", {
        "form": form,
        "story": story,
    })

@login_required
def add_character_image(request, story_id, character_id):
    story = get_object_or_404(Story, id=story_id, author=request.user)

    if request.user.profile.role != "Writer":
        return redirect("profile")

    character = get_object_or_404(
        Character,
        id=character_id,
        world__story=story
    )

    if request.method == "POST":
        form = CharacterImageForm(request.POST, request.FILES)

        if form.is_valid():
            character_image = form.save(commit=False)
            character_image.character = character
            character_image.save()
            return redirect("world_explorer", story_id=story.id)
    else:
        form = CharacterImageForm()

    return render(request, "loreverse/add_character_image.html", {
        "form": form,
        "story": story,
        "character": character,
    })

@login_required
def add_location_image(request, story_id, location_id):
    story = get_object_or_404(Story, id=story_id, author=request.user)

    if request.user.profile.role != "Writer":
        return redirect("profile")

    location = get_object_or_404(
        Location,
        id=location_id,
        world__story=story
    )

    if request.method == "POST":
        form = LocationImageForm(request.POST, request.FILES)

        if form.is_valid():
            location_image = form.save(commit=False)
            location_image.location = location
            location_image.save()
            return redirect("world_explorer", story_id=story.id)
    else:
        form = LocationImageForm()

    return render(request, "loreverse/add_location_image.html", {
        "form": form,
        "story": story,
        "location": location,
    })

@login_required
def add_creature_image(request, story_id, creature_id):
    story = get_object_or_404(Story, id=story_id, author=request.user)

    if request.user.profile.role != "Writer":
        return redirect("profile")

    creature = get_object_or_404(
        Creature,
        id=creature_id,
        world__story=story
    )

    if request.method == "POST":
        form = CreatureImageForm(request.POST, request.FILES)

        if form.is_valid():
            creature_image = form.save(commit=False)
            creature_image.creature = creature
            creature_image.save()
            return redirect("world_explorer", story_id=story.id)
    else:
        form = CreatureImageForm()

    return render(request, "loreverse/add_creature_image.html", {
        "form": form,
        "story": story,
        "creature": creature,
    })

@login_required
def toggle_chapter_like(request, story_id, chapter_id):
    story = get_object_or_404(Story, id=story_id, published=True)
    chapter = get_object_or_404(Chapter, id=chapter_id, story=story)

    like = ChapterLike.objects.filter(
        user=request.user,
        chapter=chapter
    ).first()

    if like:
        like.delete()
    else:
        ChapterLike.objects.create(
            user=request.user,
            chapter=chapter
        )

    return redirect(
        "read_chapter",story_id=story.id,chapter_id=chapter.id)