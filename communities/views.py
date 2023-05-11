from django.shortcuts import render, redirect
from .models import Comment, Recomment
from courses.models import Review
from .forms import CommentForm, RecommentForm
from courses.models import Course
from django.core.paginator import Paginator
# Create your views here.

def comment(request):
    comments = Comment.objects.order_by('-id')
    category = request.GET.get('category', None)


    if category:
        comments = comments.filter(category=category)

    context = {
        'comments': comments,
        'category': category,
    }

    return render(request, 'communities/comment_index.html', context)

def comment_detail(request, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    recomments = Recomment.objects.filter(comment=comment_pk)
    print(recomments)
    recomment_form = RecommentForm()
    # like_users_count = comment.like_users.count()
    context = {
        'comment': comment,
        'recomments': recomments,
        'recomment_form': recomment_form,
        # 'like_users_count': like_users_count,

    }

    return render(request, 'communities/comment_detail.html', context)

def comment_create(request):
    course_pk = request.GET.get('course_pk', 0)
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            if course_pk != 0:
                course = Course.objects.get(pk=course_pk)
                comment.course = course
            comment.user = request.user
            comment.save()

            return redirect('communities:comment_index')

    else:
        comment_form = CommentForm()
    context = {
        'comment_form': comment_form,
    }

    return render(request, 'communities/comment_create.html', context)

def comment_update(request, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)

    if request.user == comment.user:
        if request.method == 'POST':
            comment_form = CommentForm(request.POST, instance=comment)
            if comment_form.is_valid():
                comment_form.save()
                return redirect('communities:comment_detail', comment_pk)
        else:
            comment_form = CommentForm(instance=comment)

    else:
        return redirect('communities:comment_detail', comment_pk)
    context = {
        'comment': comment,
        'comment_form': comment_form,
    }
    return render(request, 'communities/comment_update.html', context)

def comment_delete(request, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.user == comment.user and request.method == 'POST':
        comment.delete()
        return redirect('communities:comment_index')
    

## 대댓글

def recomment_create(request, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)

    if request.method == 'POST':
        recomment_form = RecommentForm(request.POST)
        if recomment_form.is_valid():
            recomment = recomment_form.save(commit=False)
            recomment.comment = comment
            recomment.user = request.user
            recomment.save()

            return redirect('communities:comment_detail', comment_pk)

    else:
        recomment_form = RecommentForm()

    context = {
        'comment': comment,
        'recomment_form': recomment_form,
    }

    return render(request, 'communities/recomment_create.html', context)


def recomment_delete(request, comment_pk, recomment_pk):
    recomment = Recomment.objects.get(pk=recomment_pk)

    if request.user == recomment.user and request.method == 'POST':
        recomment.delete()

    return redirect('communities:recomment', comment_pk=comment_pk)


def review(request):
    reviews = Review.objects.order_by('-id')
    page = request.GET.get('page', '1')
    per_page = 5
    paginator = Paginator(reviews, per_page)
    page_obj = paginator.get_page(page)

    last = paginator.num_pages
    context = {
        'reviews': page_obj,
        'page_obj': page_obj,
        'last': last,
    }

    return render(request, 'communities\inflearn_index.html', context)

