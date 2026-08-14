from django.shortcuts import render , redirect ,  get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login , authenticate , logout
from django.db import IntegrityError
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from .models import Profile , Story , Chapter  , ReadingProgress ,ReadingHistory , CompletedStory
from .forms import ProfileForm , StoryForm , ChapterForm
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
    chapter = get_object_or_404( Chapter, id=chapter_id, story=story)

    chapters = list(story.chapters.all().order_by("chapter_number"))
    current_index = chapters.index(chapter)

    previous_chapter = None
    next_chapter = None

    if current_index > 0:
        previous_chapter = chapters[current_index - 1]

    if current_index < len(chapters) - 1:
        next_chapter = chapters[current_index + 1]

    if request.user.is_authenticated:
        ReadingProgress.objects.update_or_create( user=request.user, story=story, defaults={"chapter": chapter})
        ReadingHistory.objects.update_or_create(user=request.user,story=story)

    return render(request, "loreverse/read_chapter.html", {
        "story": story, "chapter": chapter,
        "previous_chapter": previous_chapter, "next_chapter": next_chapter
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