from django.shortcuts import render, redirect, get_object_or_404
from .models import Course, Review
from .forms import CoursesForm, ReviewForm
from django.contrib.auth.decorators import login_required
from taggit.models import Tag, TaggedItem
from communities.models import Comment
from django.core.paginator import Paginator
import random


# Create your views here.

def index(request):
    courses = Course.objects.all().order_by('-pk')
    context = {
        'courses': courses,
    }
    return render(request, 'courses/course_index.html', context)


def detail(request, course_pk):
    course = Course.objects.get(pk=course_pk)
    reviews = Review.objects.filter(course_id=course_pk)
    review_form = ReviewForm()
    if Course.objects.count() > 3:
        other_courses = random.sample(list(Course.objects.all().exclude(pk=course.pk)), 3)
    else:
        other_courses = []
    similar_courses = Course.objects.filter(tags__in=course.tags.all()).exclude(pk=course.pk)
    similar_course = random.choice(similar_courses) if similar_courses else None
    context = {
        'course': course,
        'reviews': reviews,
        'review_form': review_form,
        'other_courses': other_courses,
        'similar_course': similar_course,
    }
    return render(request, 'courses/course_detail.html', context)


@login_required
def create(request):
    if request.method == 'POST':
        form = CoursesForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.user = request.user
            course.save()
            form.save_m2m()
            return redirect('courses:detail', course.pk)
    else:
        form = CoursesForm()
    context = {
        'form': form,
    }
    return render(request, 'courses/course_create.html', context)


def comment(request, course_pk):
    course = Course.objects.get(pk=course_pk)
    context = {
        'course': course,
    }
    return render(request, 'courses/course_comment.html', context)


def courses(request):
    slug = request.GET.get('tag')
    tags = Tag.objects.all()
    if slug:
        tag = get_object_or_404(Tag, slug=slug)
        courses = Course.objects.filter(tags=tag)
    else:
        courses = Course.objects.all()
    per_page = 2
    paginator = Paginator(courses, per_page)
    courses_paginated = paginator.get_page(request.GET.get('page', '1'))
    num_page = paginator.num_pages
    context = {
        'courses': courses,
        'courses_paginated': courses_paginated,
        'num_page': num_page,
        'tags': tags,
    }
    return render(request, 'courses/course_courses.html', context)


def review_create(request, course_pk):
    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            course = Course.objects.get(pk=course_pk)
            review.course = course
            review.user = request.user
            review.save()
            return redirect('courses:detail', course_pk)
    else:
        review_form = ReviewForm()
    context = {
        'review_form': review_form,
    }
    return render(request, 'communities/comment_create.html', context)


def review_delete(request, course_pk, review_pk):
    review = Review.objects.get(pk=review_pk)
    if request.user == review.user:
        review.delete()
        return redirect('courses:detail', course_pk)
    
