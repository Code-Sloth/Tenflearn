from django.shortcuts import render, redirect
from .models import Comment, Recomment
from courses.models import Review
from .forms import CommentForm, RecommentForm
from courses.models import Course
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import Count
from django.contrib.auth import get_user_model
from django.db.models import Q

# Create your views here.

def comment(request):
    comments = Comment.objects.all().order_by('-pk')
    top_users = get_user_model().objects.filter(comment__isnull=False).annotate(comment_count=Count('comment')).order_by('-comment_count')[:7]
    
    top_tags = Comment.objects.exclude(course__isnull=True).values('course__tags__name').annotate(tag_count=Count('course__tags')).order_by('-tag_count')[:10]

    popular_comments = Comment.objects.annotate(popular=Count('like_users')).order_by('-popular')[:5]

    category = request.GET.get('category', '')
    order = request.GET.get('order','')
    search_q = request.GET.get('search-q','')
    tag_q = request.GET.get('tag-q','')

    if category:
        if category == 'all': category = ''
        comments = comments.filter(category__icontains=category)

    if search_q:
        comments = comments.filter(
            Q(title__icontains=search_q)|
            Q(content__icontains=search_q)
        )
    
    if tag_q:
        comments = comments.filter(course__tags__name__icontains=tag_q)

    if order:
        comments = comment_order(comments, order)

    context = {
        'comments': comments,
        'top_users': top_users,
        'top_tags': top_tags,
        'popular_comments': popular_comments,
    }

    return render(request, 'communities/comment_index.html', context)

def comment_order(queryset, o):
    if o == 'recent':
        return queryset.order_by('-pk')
    elif o == 'comment':
        return queryset.annotate(count_recomments=Count('recomments')).order_by('-count_recomments')
    elif o == 'like':
        return queryset.annotate(likes=Count('like_users')).order_by('-likes')

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

@login_required
def comment_create(request):
    if request.method == 'POST':
        course_pk = request.POST.get('course_pk', 0)

        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            if course_pk != '0':
                course = Course.objects.get(pk=course_pk)
                comment.course = course
            comment.user = request.user
            comment.save()

            redirect_url = reverse('communities:comment_index') + '?category=all'
            return redirect(redirect_url)
    else:
        course_pk = request.GET.get('course_pk', 0)
        comment_form = CommentForm()
        
    context = {
        'comment_form': comment_form,
        'course_pk': course_pk,
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
        redirect_url = reverse('communities:comment_index') + '?category=all'
        return redirect(redirect_url)
    

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
    reviews_count = reviews.count()
    context = {
        'reviews_count': reviews_count,
        # 'reviews': page_obj,
        'page_obj': page_obj,
        'last': last,
    }

    return render(request, 'communities\inflearn_index.html', context)

