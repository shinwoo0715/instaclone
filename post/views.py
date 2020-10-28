from django.shortcuts import render , get_object_or_404 , redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .forms import PostForm , CommentForm
from django.contrib import messages
from django.views.decorators.http import require_POST
import json
from django.http import HttpResponse
from django.core.paginator import Paginator , PageNotAnInteger , EmptyPage

from .models import Post , Like , Comment , Tag
from django.db.models import Count



def post_list(request , tag=None):
    post_list = Post.objects.all()

    paginator = Paginator(post_list , 3) # post_list를 3개만 뿌려라 ok?
    page_num = request.POST.get("page")

    try: 
        posts = paginator.page(page_num)
    
    except PageNotAnInteger: # page 파라미터가 int가 아니라면 ~ page를 1로 바꾸어라
        posts = paginator.page(1)
    
    except EmptyPage: # 페이지를 넘어서면 마지막 페이지를 보여준다.      
        posts = paginator.page(paginator.num_pages)
    
    comment_form = CommentForm()

    if request.is_ajax(): # request가 ajax인지를 확인하고요 
        return  render(request , 'post/post_list_ajax.html' , {
            'posts' : posts,
            'comment_form' : comment_form
        })



    if request.user.is_authenticated: # 사용자가 인증이 되었다면
        username = request.user
        user = get_object_or_404(get_user_model() , username=username)
        user_profile = user.profile

        following_set = request.user.profile.get_following
        following_post_list = Post.objects.filter(author__profile__in=following_set)

        print("following_post_list : " ,following_post_list)

        print("--------- post_list in views.py --------")
        print("user_profile",user_profile)
        print("posts",posts)
        print("comment_form",comment_form)
        print("following_post_list",following_post_list)
        print("\n\n")
        return render(request , 'post/post_list.html' , {
            'user_profile' : user_profile,
            'posts' : posts, 
            'comment_form' : comment_form,
            'following_post_list' : following_post_list,
        })
    else :
        return render(request , 'post/post_list.html' , {
            'posts' : post_list,
        })


# 로그인 기능을 구현해놨기 때문에 로그인기능을 불러오도록 하자.
@login_required
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            print("데이터 유효")
            post = form.save(commit=False) # 중복 db를 방지하기 위해 commit을 False로 둔다.
            post.author = request.user
            post.save()
            # post.tag_save()
            messages.info(request , '새 글이 등록 되었습니다.')
            return redirect('post:post_list')
    
    else:
        form = PostForm()
    
    return render(request , 'post/post_new.html' , {
        'form' : form,

    })

@login_required
def post_edit(request , pk): # 수정 
    post = get_object_or_404(Post , pk=pk)
    if post.author != request.user: # 수정할려했는데 post를쓴 저자와 현재 저자가 다르면 post_list로 돌아가라
        messages.warning(request , '잘못된 접근 입니다.') 
        return redirect('post:post_list')
    
    if request.method == 'POST': # 정상적인 접근을 했다면 그러니까 수정을 했다면 
        form = PostForm(request.POST , request.FILES ,  instance=post)
        if form.is_valid():
            post = form.save()
            # post.tag_set.clear()
            # post.tag_save()
            messages.success(request , '수정완료!') 
            return redirect("post:post_list")
    
    else:
        form = PostForm(instance=post)
    
    return render(request , 'post/post_edit.html' , {
        'post' : post,
        'form' : form
    })

@login_required
def post_delete(request , pk):
    post = get_object_or_404(Post , pk=pk)
    if post.author != request.user or request.method == 'GET':  # url을 통해서 db에 접근을 원천적으로 방어할수 있다.
        messages.warning(request , '잘못된 접근입니다.')
        return redirect('post:post_list')

    if request.method == 'POST':
        post.delete() 
        print("post가 삭제되었습니다.")
        messages.success(request, '삭제완료')
        return redirect('post:post_list')
    
        


@login_required # 로그인 된상태에서만 작동
@require_POST # POST방식으로만 내용을 받을 것이다.
def post_like(request):
    pk = request.POST.get('pk' , None)
    post = get_object_or_404(Post , pk=pk)
    # 이게 좀 중요한데 user간의 일종의 스위치를 만드는것이다.
    post_like , post_like_created = post.like_set.get_or_create(user=request.user)
    
    if not post_like_created:
        print("post_like_create는 False를 반환")
        post_like.delete()
        message = '좋아요 취소'
    else :
        print("post_like_create는 True를 반환")
        message = '좋아요'

    context = {'like_count' : post.like_count,
                'message' : message}

    return HttpResponse(json.dumps(context)  , content_type='application/json')

@login_required 
@require_POST
def post_bookmark(request):
    pk = request.POST.get('pk' , None)
    post = get_object_or_404(Post , pk=pk)
    # 이게 좀 중요한데 user간의 일종의 스위치를 만드는것이다.
    post_bookmark , post_bookmark_created = post.bookmark_set.get_or_create(user=request.user)
    
    if not post_bookmark_created:
        post_bookmark.delete()
        message = '북마크 취소'
    else :
        message = '북마크'

    context = {'bookmark_count' : post.bookmark_count,
                'message' : message}

    return HttpResponse(json.dumps(context)  , content_type='application/json') 


@login_required
def comment_new(request):
    pk = request.POST.get('pk')
    post = get_object_or_404(Post , pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return render(request , 'post/comment_new_ajax.html' , context={
                'comment' : comment,
            })
    return redirect('post:post_list')


@login_required
def comment_delete(request):
    pk = request.POST.get('pk')
    comment = get_object_or_404(Comment , pk=pk)
    if request.method == 'POST' and request.user == comment.author:
        comment.delete()
        message = '삭제완료'
        status = 1
    
    else :
        message = '잘못된 접근입니다' 
        status =  0 
    return HttpResponse(json.dumps({'message' : message, 'status' : status }) , content_type='application/json')