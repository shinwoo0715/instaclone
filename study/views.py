from django.shortcuts import render, redirect, get_object_or_404

from post.models import Post


def index(request):
    print("index.html 진입")
    return render(request, 'index.html')


def layout(request):
    return render(request, 'layout.html')


def post_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post_like, post_like_created = post.like_set.get_or_create(user=request.user)

    if not post_like_created:
        post_like.delete()

    return redirect('post:post_list')


def game(request):
    return render(request, 'game/guess.html')
