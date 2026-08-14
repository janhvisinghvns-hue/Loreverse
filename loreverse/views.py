from django.shortcuts import render , redirect ,  get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login , authenticate , logout
from django.db import IntegrityError
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from .models import Profile , Story , Chapter
from .forms import ProfileForm , StoryForm , ChapterForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash


def index(request):
    return render(request, "loreverse/index.html")


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
    if request.method == "POST":
        form = StoryForm(request.POST, instance=story)
        if form.is_valid():
            form.save()
            return redirect("my_stories")
    else:
        form = StoryForm(instance=story)
    return render(request, "loreverse/edit_story.html", {"form": form, "story": story})

@login_required
def delete_story(request, story_id):
    story = get_object_or_404(Story, id=story_id, author=request.user)
    if request.method == "POST":
        story.delete()
        return redirect("my_stories")
    return render(request, "loreverse/delete_story.html", {"story": story})

@login_required
def publish_story(request, story_id):
    story = get_object_or_404(Story, id=story_id, author=request.user)
    if request.method == "POST":
        story.published = True
        story.save()
    return redirect("my_stories")

def published_stories(request):
    stories = Story.objects.filter(published=True)
    return render(request, "loreverse/published_stories.html", {"stories": stories})

def story_detail(request, story_id):
    story = get_object_or_404(Story, id=story_id, published=True)
    chapters = story.chapters.all().order_by("chapter_number")
    return render(request, "loreverse/story_detail.html", {"story": story, "chapters": chapters})

@login_required
def create_chapter(request, story_id):
    story = get_object_or_404(Story, id=story_id, author=request.user)
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