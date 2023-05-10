from django.shortcuts import render, redirect
from .models import Comment, Recomment, Review
from .forms import CommentForm, RecommentForm, ReviewForm
from courses.models import Course
# Create your views here.

def comment(request):
    reviews = Comment.objects.all()

    context = {
        'reviews': reviews,
    }

    return render(request, 'communities/comment_index.html', context)

def comment_detail(request, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)

    context = {
        'comment': comment,
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

def recomment(request, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    recomments = comment.recomment_set.all()

    context = {
        'comment': comment,
        'recomments': recomments,
    }

    return render(request, 'communities/comment_detail.html', context)

def recomment_create(request, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)

    if request.method == 'POST':
        recomment_form = RecommentForm(request.POST)
        if recomment_form.is_valid():
            recomment = recomment_form.save(commit=False)
            recomment.comment = comment
            recomment.user = request.user
            recomment.save()

            return redirect('communities:recomment', comment_pk=comment_pk)

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





## 리뷰

def review(request):
    reviews = Review.objects.all()

    context = {
        'reviews': reviews,
    }

    return render(request, 'communities\inflearn_index.html', context)


def review_create(request):
    course_pk = request.GET.get('course_pk')

    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            course = Course.objects.get(pk=course_pk)
            review.course = course
            review.user = request.user
            review.save()

            return redirect('#')

    else:
        review_form = ReviewForm()
    context = {
        'review_form': review_form,
    }

    return render(request, 'communities/comment_create.html', context)


def review_delete(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    course_pk = request.GET.get('course_pk', 0)
    if request.user == review.user and request.method == 'POST':
        review.delete()
        return redirect('courses:detail', course_pk)