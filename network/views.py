from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse

import json
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import User,Post,Follow


def index(request):
    posts = Post.objects.all().order_by("id").reverse()
    paginatedPosts= Paginator(posts,10)
    pageNumber = request.GET.get("page")
    singlePagePosts =  paginatedPosts.get_page(pageNumber)



    return render(request, "network/index.html",{
        "posts":singlePagePosts,
    })



# for creating new Post
def newPost(request):
    if request.method == "POST":
        user = request.user
        content = request.POST.get("content")
        Post.objects.create(user = user,content = content)
        return HttpResponseRedirect(reverse("index"))


# for displaying profile of user
def displayProfile(request,username):
    if request.method =="GET":
        requestUser =request.user
        postUser  = get_object_or_404(User,username = username)
        posts = Post.objects.filter(user = postUser)
        paginatedPosts= Paginator(posts,10)
        pageNumber = request.GET.get("page")
        singlePagePosts =  paginatedPosts.get_page(pageNumber)
        # display follow button or not
        displayFollow = requestUser!=postUser
        isFollowing = False
        if requestUser.is_authenticated:
            isFollowing = Follow.objects.filter(user=postUser, following=requestUser).exists()
        followers = Follow.objects.filter(user = postUser)
        following = Follow.objects.filter(following = postUser)
        return render(request, "network/profile.html",{
            "posts":singlePagePosts,
            "postUser":postUser,
            "displayFollow":displayFollow,
            "isFollowing":isFollowing,
            "followers" :followers,
            "following":following
        })

# for following a user
def follow(request,id):
    requestUser = request.user
    postUser = User.objects.get(pk = id)
    Follow.objects.create(user = postUser,following = requestUser)
    return redirect("profile", username=postUser.username)

# for unfollowing a user
def unfollow(request, id):
    requestUser = request.user
    postUser = User.objects.get(pk = id)
    temp = Follow.objects.filter(user = postUser,following = requestUser)
    temp.delete()
    return redirect("profile", username=postUser.username)


# for displaying posts of people the user follows
def displayFollowing(request):
    user = request.user
    following = Follow.objects.filter(following = user)
    posts = []
    for follow in following:
        posts.extend(Post.objects.filter(user = follow.user).order_by("id").reverse())
    paginatedPosts= Paginator(posts,10)
    pageNumber = request.GET.get("page")
    singlePagePosts =  paginatedPosts.get_page(pageNumber)
    return render(request,"network/following.html",{
        "posts":singlePagePosts
    })

# for editing post
@login_required
@csrf_exempt
def edit(request,id):
    try:
        post = Post.objects.get( pk= id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    if request.method == "GET":
        return JsonResponse(Post.serialize())
    
    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("content") is not None:
            post.content = data["content"]
            post.save()
        return JsonResponse(status=200)
    
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)

@csrf_exempt
@login_required
def updateLike(request,id):
    user = request.user
    try:
        post = Post.objects.get(pk = id)
    except Post.DoesNotExist:
        return JsonResponse({"message":"Post does not exist"},status =404)
    
    if post.likes.filter(id = user.id).exists():
        post.likes.remove(user)
        hasLiked = False
    else:
        post.likes.add(user)
        hasLiked =True
    post.save()
    totalLikes = post.numberOfLikes()
    return JsonResponse({"hasLiked":hasLiked,"numberOfLikes":totalLikes},status = 202)


    


# def like(request,id):
#     user =request.user
#     post = Post.objects.get(pk = id)
#     Like.objects.create(user = user,post = post)
#     return JsonResponse({"message":"Liked successfully"})

# def unlike(request,id):
#     user =request.user
#     post = Post.objects.get(pk = id)
#     like = Like.objects.filter(user = user,post = post)
#     like.delete()
#     return JsonResponse({"message":"Unliked successfully!"})


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


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


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
