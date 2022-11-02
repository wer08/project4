from crypt import methods
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django import forms
import json


from .models import Following, User, Post, Like


from django.views.decorators.csrf import csrf_protect

from network import models


#view to render profile
def profile(request,user):
    print(user)
    flag = True
    author = User.objects.get(username = user)
    followings = request.user.followings.all()
    for following in followings:
        if following.followed == author:    
            flag = False
    followers = author.followers.count()
    author.number_followers = followers
    author.save()

    posts = Post.objects.filter(author = author).order_by('-time_stamp')

    pagin = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = pagin.get_page(page_number)
    return render(request, "network/profile.html", {
        'posts':page_obj,
        'author': author,
        'flag': flag
    })

#view to follow and unfollow users
def follow(request,user):
    
    flag = True
    author = User.objects.get(username = user)
    followings = request.user.followings.all()
    for following in followings:
        if following.followed == author:    
            flag = False

    if flag:
        follow = Following(follower = request.user, followed = author)
        follow.save()
    else:
        Following.objects.get(follower = request.user, followed = author).delete()

    return HttpResponseRedirect(reverse("profile",kwargs={
        'user': user
    }))


def posts(request):

    posts = Post.objects.all()


    return JsonResponse([post.serialize() for post in posts], safe=False)

@csrf_protect
def post(request,post_id):
    post = Post.objects.get(pk = post_id)

    if request.method == "PUT":

        data = json.loads(request.body) 
        if data.get("body") is not None:
            post.body = data['body']
        elif data.get("likes") is not None:
            liker_id = data['liker']
            liker = User.objects.get(pk = liker_id)
            if not liker in likers: 
                print("no liker")
                post.likes = data['likes']
        post.save()
        return HttpResponse(status=204)
    else:
        return JsonResponse(post.serialize())

@login_required
def like(request,post):
    post = Post.objects.get(pk = post)
    if request.method == "POST":
        likers_likes = post.likers.all()
        print(likers_likes)
        likers = []
        for like in likers_likes:
            liker = like.liker
            likers.append(liker)
        number_of_likes = len(likers)
        data = json.loads(request.body) 
        liker_id = data['liker']
        liker = User.objects.get(pk = liker_id)
        try:
            like = Like.objects.get(liker = liker, liked_post = post)
        except models.Like.DoesNotExist:
            like = Like(liker = liker, liked_post = post)
            like.save()
            number_of_likes += 1
            post.likes = number_of_likes
            post.save()
        return HttpResponse(status=204)
    else:
        return JsonResponse(post.serialize())

@login_required
def unlike(request,post):
    post = Post.objects.get(pk = post)
    if request.method == "DELETE":
        data = json.loads(request.body)
        liker_id = data["liker"]
        liker = User.objects.get(pk = liker_id)
        try:
            like = Like.objects.get(liked_post = post,liker=liker)
            like.delete()
            post.likes -= 1
            post.save()
            return HttpResponse(status=204)
        except models.Like.DoesNotExist:
            print("cant'unlike")
            return HttpResponse(status=400)
            
    else:
        return JsonResponse(post.serialize())
    

#view to render following page
@login_required
def following(request):
    followed = request.user.followings.all().values_list('followed', flat=True)
    
    posts = Post.objects.filter(author__in=followed).order_by('-time_stamp')
    pagin = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = pagin.get_page(page_number)
    
    return render(request, "network/following.html", {
        'posts':page_obj,
    })


#view to add post
def new_post(request):
    if request.method == "POST":
        body = request.POST["new"]
        author = request.user
        post = Post(body = body, author = author)
        post.save()

    return HttpResponseRedirect(reverse("index"))




#view to render main page
def index(request):

    posts = Post.objects.order_by('-time_stamp')
    pagin = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = pagin.get_page(page_number)
    user = request.user
    liked = Like.objects.filter(liker = user)
    liked_posts = []
    for like in liked:
        liked_posts.append(like.liked_post)
    
    return render(request, "network/index.html", {
        'posts':page_obj,
        'liked_posts':liked_posts
    })

#view to render login page with GET method and login user with POST method
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")

#view to logout user 
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

#view to render register page with get method and register user with POST method
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
