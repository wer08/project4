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


#view to render profile
def profile(request,user):
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
    return render(request, "network/profile.html", {
        'posts':posts,
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

@login_required
def like(request,post):
    if request.method == 'POST':
        
        flag = True
        post = Post.objects.get(pk = post)
        print(f"test: {post.likers}")
        likes = request.user.liked.all()
        for like in likes:
            if like.liked_post == post:    
                flag = False

        if flag:
            like = Like(liker = request.user, liked_post = post)
            like.save()
        else:
            Like.objects.get(liker = request.user, liked_post = post).delete()

        return HttpResponse(status=204)

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
            post.likes = data['likes']
        post.save()
        return HttpResponse(status=204)
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
    likers = []
    for post in page_obj:
        post_like = post.likers.all()
        for like in post_like:
            like = like.liker
            likers.append(like)





    
    return render(request, "network/index.html", {
        'posts':page_obj,
        'likers':likers
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
