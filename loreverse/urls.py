from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile_view, name="profile"),
    path("change_password/", views.change_password_view, name="change_password"),
    path("create_story/", views.create_story, name="create_story"),
    path("my_stories/", views.my_stories, name="my_stories"),
    path("edit_story/<int:story_id>/", views.edit_story, name="edit_story"),
    path("delete_story/<int:story_id>/", views.delete_story, name="delete_story"),
    path("publish_story/<int:story_id>/", views.publish_story, name="publish_story"),
    path("stories/", views.published_stories, name="published_stories"),
    path("stories/<int:story_id>/", views.story_detail, name="story_detail"),
    path("stories/<int:story_id>/create_chapter/", views.create_chapter, name="create_chapter"),
]