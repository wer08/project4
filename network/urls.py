
from unicodedata import name
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_post", views.new_post, name="new_post"),
    path("profile/<str:user>", views.profile, name="profile"),
    path("profile/follow/<str:user>", views.follow, name="follow"),
    path("following", views.following, name="following"),
    path("posts", views.posts, name="posts"),
    path("post/<int:post_id>", views.post, name="post"),
    path("like/<int:post>", views.like, name="like"),
    path("unlike/<int:post>", views.unlike, name="unlike")
]
