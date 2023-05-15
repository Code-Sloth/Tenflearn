from django.shortcuts import render, redirect, get_object_or_404
from .models import Course, Review, Quiz, StudentAnswer
from .forms import CoursesForm, ReviewForm, QuizForm, QnAForm, QnAFormSet
from django.forms import formset_factory
from django.contrib.auth.decorators import login_required
from taggit.models import Tag
from django.core.paginator import Paginator
import random
from django.db.models import Count
from django.db.models import Q

# Create your views here.

def index(request):
    courses = Course.objects.all().order_by('-pk')
    sorted_star_courses = Course.objects.all().order_by('-star')
    sorted_enrolment_courses = Course.objects.annotate(num_enrolment_users=Count('enrolment_users')).order_by('-num_enrolment_users')
    if request.user.is_authenticated:
        enrolled_courses = Course.objects.filter(enrolment_users=request.user)
        if enrolled_courses:
            enrolled_course_tags = enrolled_courses.values_list('tags', flat=True).distinct()
            similar_courses = Course.objects.filter(Q(tags__in=enrolled_course_tags) & ~Q(enrolment_users=request.user)).distinct()
        else:
            similar_courses = None
    else:
        similar_courses = None
    context = {
        'courses': courses,
        'sorted_star_courses': sorted_star_courses,
        'sorted_enrolment_courses' : sorted_enrolment_courses,
        'similar_courses': similar_courses,
    }
    return render(request, 'courses/course_index.html', context)


def detail(request, course_pk):
    course = Course.objects.get(pk=course_pk)
    reviews = Review.objects.filter(course_id=course_pk)
    review_form = ReviewForm()

    if Course.objects.count() > 4:
        other_courses = random.sample(list(Course.objects.all().exclude(pk=course.pk)), 4)
    else:
        other_courses = Course.objects.all().exclude(pk=course.pk)

    similar_courses = Course.objects.filter(tags__in=course.tags.all()).exclude(pk=course.pk)

    if similar_courses.count() > 4:
        similar_courses = similar_courses[::3]

    star_percentage = []
    if reviews:
        for x in range(1, 6):
            star_percentage.append(round(reviews.filter(star=x).count()*100/reviews.count(), 1))
    else:
        star_percentage = [0, 0, 0, 0, 0]
    context = {
        'course': course,
        'reviews': reviews,
        'review_form': review_form,
        'other_courses': other_courses,
        'similar_courses': similar_courses,
        'star_percentage': star_percentage,
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


@login_required
def update(request, course_pk):
    course = Course.objects.get(pk=course_pk)
    if request.user == course.user:
        if request.method == 'POST':
            form = CoursesForm(request.POST, request.FILES, instance=course)
            if form.is_valid():
                form.save()
                return redirect('courses:detail', course.pk)
        else:
            form = CoursesForm(instance=course)
    else:
        return redirect('courses:index')
    context = {
        'course': course,
        'form': form,
    }
    return render(request, 'courses/course_update.html', context)


@login_required
def delete(request, course_pk):
    course = Course.objects.get(pk=course_pk)
    if request.user == course.user:
        course.delete()
        return redirect('courses:index')


def comment(request, course_pk):
    course = Course.objects.get(pk=course_pk)
    comment_type = request.GET.get('type')
    q = request.GET.get('q')

    course_comments = course.comments.all()
    if comment_type:
        course_comments = course_comments.filter(category=comment_type)

    if q:
        course_comments = course_comments.filter(
            Q(title__icontains=q)|
            Q(content__icontains=q)|
            Q(course__tags__name__icontains=q)
        ).distinct()

    context = {
        'course': course,
        'course_comments': course_comments,
        'comment_type': comment_type,
    }
    return render(request, 'courses/course_comment.html', context)

def courses(request):
    tags = Tag.objects.all()
    # 선택한 태그들 가져옴
    selected_slugs = request.GET.get('tags')
    if selected_slugs:
        selected_tags = selected_slugs.split(',')
        courses = Course.objects.filter(tags__slug__in=selected_tags).distinct()
        
    else:
        courses = Course.objects.all()

    # 정렬
    order = request.GET.get('sort')
    if order == 'rating':
        courses = courses.order_by('-star')
    elif order == 'enrollment':
        courses = courses.order_by('-enrolment_users')
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
    

def video(request, course_pk):
    course = Course.objects.get(pk=course_pk)
    context = {
        'course': course,
    }
    return render(request, 'courses/course_video.html', context)


@login_required
def quiz_create(request, course_pk):
    course = Course.objects.get(pk=course_pk)
    quiz_form = QuizForm(request.POST or None)
    QnAFormSet = formset_factory(QnAForm, extra=5)
    qna_formset = QnAFormSet(request.POST or None)

    if request.method == 'POST':
        if quiz_form.is_valid() and qna_formset.is_valid():
            quiz = quiz_form.save(commit=False)
            quiz.course = course
            quiz.created_by = request.user
            quiz.save()
            for form in qna_formset:
                if form.is_valid():
                    qna = form.save(commit=False)
                    qna.quiz = quiz
                    qna.save()
            return redirect('courses:detail', course_pk)

    context = {
        'quiz_form': quiz_form,
        'qna_formset': qna_formset,
        'course': course,
    }
    return render(request, 'courses/course_quiz_create.html', context)


def quiz(request, course_pk, quiz_pk):
    quiz = Quiz.objects.get(pk=quiz_pk)
    questions = quiz.questions.all()

    if request.method == 'POST':
        student = request.user
        for question in questions:
            student_answer, created = StudentAnswer.objects.get_or_create(
                qna=question,
                student=student
            )
            student_answer.is_correct = question.answer_text == request.POST.get(str(question.id))
            student_answer.save()
        return redirect('courses:quiz_result', course_pk, quiz_pk)

    context = {
        'quiz': quiz,
        'questions': questions,
    }
    return render(request, 'courses/course_quiz.html', context)


@login_required
def quiz_result(request, course_pk, quiz_pk):
    quiz = Quiz.objects.get(id=quiz_pk)
    total_questions = quiz.questions.count()
    student_answers = StudentAnswer.objects.filter(qna__quiz=quiz, student=request.user)
    num_correct_answers = student_answers.filter(is_correct=True).count()
    num_incorrect_answers = student_answers.filter(is_correct=False).count()
    context = {
        'quiz': quiz,
        'total_questions': total_questions,
        'num_correct_answers': num_correct_answers,
        'num_incorrect_answers': num_incorrect_answers,
    }
    return render(request, 'courses/course_quiz_result.html', context)

