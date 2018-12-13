from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import Http404
from django.http import HttpResponseRedirect
from django.db.models import Count
from django.contrib import messages
from blog.models import User, Post, Comment, Favorite, Like, Follow
from blog.forms import PostForm, ContactForm, CommentForm
from blog.serializers import PostSerializer, CommentSerializer, FollowSerializer, UserSerializer, LikeSerializer, FavoriteSerializer
from registration.backends.simple.views import RegistrationView
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response

def index(request):
    posts = Post.objects.all().annotate(num_likes=Count('likes')).order_by('-num_likes', '-created')

    return render(request, 'index.html', {'posts': posts})

def post_detail(request, slug):
    post = Post.objects.get(slug=slug)
    comments = post.comments.all().order_by('-created')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            message = f"Your comment has been added to '{post.title}'!"
            messages.add_message(request, messages.SUCCESS, message)

            return redirect('post_detail', slug)
    else:
        form = CommentForm()
    return render(request, 'posts/post_detail.html', {
        'post': post,
        'comments': comments,
        "form": form,
        "slug": slug,
    })

def create_hail(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('accounts/login')

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            message = f"Your hail has been added!"
            messages.add_message(request, messages.SUCCESS, message)

            return redirect('home')
    else:
        form = PostForm()

    return render(request, 'posts/create_post.html', {
        'form': form,
    })

@login_required
def edit_post(request, slug):
    post = Post.objects.get(slug=slug)
    if post.user != request.user:
        raise Http404
    if request.method == 'POST':
        form = PostForm(data=request.POST, instance=post)
        if form.is_valid():
            form.save()
            message = f"'{post.title}' was edited successfully!"
            messages.add_message(request, messages.SUCCESS, message)

            return redirect('posts/post_detail', slug=post.slug)
    else:
        form = PostForm(instance=post)

    return render(request, 'posts/edit_post.html', {
        'post': post,
        'form': form,
    })

def add_comment_to_post(request, slug):
    post = Post.objects.get(slug=slug)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            message = f"Your comment has been added to '{post.title}'!"
            messages.add_message(request, messages.SUCCESS, message)
            return redirect('post_detail', slug)
    else:
        form = CommentForm()

    return render(request, 'post_detail.html', {
        'post': post,
        'form': form,
        'slug': slug,
    })

@login_required
def edit_comment(request, slug, pk):
    post = Post.objects.get(slug=slug)
    comment = Comment.objects.get(pk=pk)
    if comment.user != request.user:
        raise Http404
    if request.method == 'POST':
        form = CommentForm(data=request.POST, instance=comment)
        if form.is_valid():
            form.save()
            message = f"Your comment has been edited!"
            messages.add_message(request, messages.SUCCESS, message)
            return redirect('post_detail', slug=post.slug)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'edit_comment.html', {
        'comment': comment,
        'form': form,
    })

def get_post_list(request, header, posts):
    fav_posts = posts.annotate(num_favorites=Count('favorites'))
    favorite_posts = []
    if request.user.is_authenticated:
        favorite_posts = request.user.favorite_posts.all()

    return render(request, 'index.html', {
        'favorite_posts': favorite_posts
    })

def delete_comment(request, slug, pk):
    post = Post.objects.get(slug=slug)
    comment = Comment.objects.get(pk=pk)
    comment.delete()
    message = f"Your comment has been removed from '{post.title}'!"
    messages.add_message(request, messages.WARNING, message)

    return redirect('post_detail', slug)

def like(request, slug):
    post = Post.objects.get(slug=slug)
    if post in request.user.liked_posts.all():
        liked = True
        post.likes.get(user=request.user).delete()
        message = f"Your like has been removed from the post '{post.title}'!"
        messages.add_message(request, messages.WARNING, message)
    else:
        liked = False
        post.likes.create(user=request.user)
        message = f"You added a like for the post '{post.title}'!"
        messages.add_message(request, messages.SUCCESS, message)

def like_index(request, slug=None):
    like(request, slug)

    return redirect('home')

def like_detail(request, slug):
    like(request, slug)

    return redirect('post_detail', slug)

# custom views for searching or seeing user profile related activity
def search(request):
    query = request.GET.get('search')
    posts = Post.objects.filter(title__icontains=query)

    return render(request, 'index.html', {'posts': posts})

def liked(request):
    liked_posts = request.user.liked_posts.all()

    return render(request, 'liked.html', {'liked_posts': liked_posts})

def commented(request):
    commented_posts = request.user.user_comments.all().order_by('-created').distinct()

    return render(request, 'comments.html', {'commented_posts': commented_posts})

def posted(request):
    posts = Post.objects.filter(user=request.user).order_by('-created')
    # posts = request.user.user.all().order_by('-created')

    return render(request, 'posts/posted.html', {'posts': posts})

class ListCreatePost(APIView):
    def get(self, request, format=None):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@require_POST
@login_required
def toggle_favorite(request, slug):
    # get the post to toggle favorite on
    post = Post.objects.get(slug=slug)
    # see if current user has this post as a favorite
    if post in request.user.favorite_posts.all():
        # if so, delete favorite
        favorite = False
        post.favorites.get(user=request.user).delete()
        message = f"You have unfavorited '{post}'."
    else:
        # else create favorite
        favorite = True
        post.favorites.create(user=request.user)
        message = f"You have favorited '{post}'."

    if request.is_ajax():
        return JsonResponse({"slug": slug, "favorite": favorite, "num_of_favorites": post.favorites.count()})

    messages.add_message(request, messages.INFO, message)
    return redirect('home')

@require_POST
@login_required
def toggle_like(request, slug):
    # get the post to toggle like on
    post = Post.objects.get(slug=slug)
    # see if current user has this post as a like
    if post in request.user.liked_posts.all():
        # if so, delete favorite
        like = False
        post.likes.get(user=request.user).delete()
        message = f"You have unliked '{post}'."
    else:
        # else create like
        like = True
        post.likes.create(user=request.user)
        message = f"You have liked '{post}'."

    if request.is_ajax():
        return JsonResponse({"slug": slug, "like": like, "num_of_likes": post.likes.count()})

    messages.add_message(request, messages.INFO, message)
    return redirect('home')

def user_profile(request, username):
    profile = User.objects.get(username=username)

    return render(request, 'user_profile.html', {"profile": profile, "username": username})

@require_POST
@login_required
def toggle_follow(request, pk):
    # get the post to toggle follow on
    profile = User.objects.get(pk=pk)
    # see if current user has this post as a follow
    if profile in request.user.users_followed.all():
        # if so, delete follow
        follow = False
        following = 'Follow'
        profile.followed_by.get(following=request.user).delete()
        message = f"You have unfollowed '{profile}'."
    else:
        # else create follow
        follow = True
        following = 'Unfollow'
        Follow.objects.create(following=request.user, followed=profile)
        message = f"You have followed '{profile}'."

    if request.is_ajax():
        return JsonResponse({"pk": pk, "follow": follow,})

    messages.add_message(request, messages.INFO, message)
    return redirect('home')

class FollowListCreateView(generics.ListCreateAPIView):
    serializer_class = FollowSerializer

    def get_queryset(self):
        return self.request.user.is_following

    def perform_create(self, serializer):
        serializer.save(following=self.request.user)

class FollowDestroyView(generics.DestroyAPIView):
    lookup_field = 'followed__username'
    lookup_url_kwarg = 'username'
    
    def get_queryset(self):
        return self.request.user.is_following

    
# def propose_new_post(request):
#     if request.method == "POST":
#         form = ProposedPostForm(request.POST)
#         if form.is_valid():
#             post = form.save()
#             messages.add_message(
#                 request, messages.SUCCESS,
#                 f"Your recommendation of {post} has been noted. Thanks!")
#             return redirect(to='post_list')
#     else:
#         form = ProposedPostForm()

#     return render(request, "posts/propose_new_post.html", {"form": form})
