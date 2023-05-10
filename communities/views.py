from django.shortcuts import render, redirect
from .models import Comment, Recomment, Review
from .forms import CommentForm, RecommentForm, ReviewForm
from courses.models import Course
# Create your views here.

def comment(request):
    comments = Comment.objects.all()

    context = {
        'comments': comments,
    }

    return render(request, 'communities/comment_index.html', context)

def comment_detail(request, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)

    context = {
        'comment': comment,
    }

    return render(request, 'communities/comment_detail.html', context)

def comment_create(request):
# def comment_create(request, course_pk):
    # if course_pk:
    #     course = Course.objects.get(pk=course_pk)
    # else:
    #     course =
        


    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            # comment.course = course
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