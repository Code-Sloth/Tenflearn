from django.shortcuts import render, redirect, get_object_or_404
from .models import Course, Review, Quiz, StudentAnswer, Url
from .forms import CoursesForm, ReviewForm, QuizForm, QnAForm, QnAFormSet
from django.forms import formset_factory
from django.contrib.auth.decorators import login_required
from taggit.models import Tag
from django.core.paginator import Paginator
import random
from django.db.models import Count
from django.db.models import Q
from functools import reduce
import requests
import os
KAKAO_KEY = os.getenv('KAKAO_KEY')

# Create your views here.


def index(request):
    courses = Course.objects.all().order_by("-pk")
    sorted_star_courses = Course.objects.all().order_by("-star")
    sorted_enrolment_courses = Course.objects.annotate(
        num_enrolment_users=Count("enrolment_users")
    ).order_by("-num_enrolment_users")
    if request.user.is_authenticated:
        enrolled_courses = Course.objects.filter(enrolment_users=request.user)
        if enrolled_courses:
            enrolled_course_tags = enrolled_courses.values_list(
                "tags", flat=True
            ).distinct()
            similar_courses = Course.objects.filter(
                Q(tags__in=enrolled_course_tags) & ~Q(enrolment_users=request.user)
            ).distinct()
        else:
            similar_courses = None
    else:
        similar_courses = None

    context = {
        "courses": courses,
        "sorted_star_courses": sorted_star_courses,
        "sorted_enrolment_courses": sorted_enrolment_courses,
        "similar_courses": similar_courses,
    }
    return render(request, "courses/course_index.html", context)


def detail(request, course_pk):
    course = Course.objects.get(pk=course_pk)
    reviews = Review.objects.filter(course_id=course_pk)
    review_form = ReviewForm()
    urls = Url.objects.filter(course_id=course_pk)
    other_courses = Course.objects.filter(user=course.user)

    if other_courses.count() > 4:
        other_courses = random.sample(
            list(other_courses.exclude(pk=course.pk)), 4
        )
    else:
        other_courses = other_courses.exclude(pk=course.pk)

    similar_courses = Course.objects.filter(tags__in=course.tags.all()).exclude(
        pk=course.pk
    )

    if similar_courses.count() > 4:
        similar_courses = similar_courses[::3]

    star_percentage = []
    if reviews:
        for x in range(1, 6):
            star_percentage.append(
                round(reviews.filter(star=x).count() * 100 / reviews.count(), 1)
            )
    else:
        star_percentage = [0, 0, 0, 0, 0]
    context = {
        "course": course,
        "reviews": reviews,
        "urls": urls,
        "review_form": review_form,
        "other_courses": other_courses,
        "similar_courses": similar_courses,
        "star_percentage": star_percentage,
    }
    return render(request, "courses/course_detail.html", context)


@login_required
def create(request):
    if request.method == "POST":
        form = CoursesForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.user = request.user
            course.save()
            form.save_m2m()
            return redirect("courses:detail", course.pk)
    else:
        form = CoursesForm()
    context = {
        "form": form,
    }
    return render(request, "courses/course_create.html", context)


@login_required
def update(request, course_pk):
    course = Course.objects.get(pk=course_pk)
    if request.user == course.user:
        if request.method == "POST":
            form = CoursesForm(request.POST, request.FILES, instance=course)
            if form.is_valid():
                form.save()
                return redirect("courses:detail", course.pk)
        else:
            form = CoursesForm(instance=course)
    else:
        return redirect("courses:index")
    context = {
        "course": course,
        "form": form,
    }
    return render(request, "courses/course_update.html", context)


@login_required
def delete(request, course_pk):
    course = Course.objects.get(pk=course_pk)
    if request.user == course.user:
        course.delete()
        return redirect("courses:index")


def comment(request, course_pk):
    course = Course.objects.get(pk=course_pk)
    comment_type = request.GET.get("type")
    q = request.GET.get("q")

    course_comments = course.comments.all()
    if comment_type:
        course_comments = course_comments.filter(category=comment_type)

    if q:
        course_comments = course_comments.filter(
            Q(title__icontains=q)
            | Q(content__icontains=q)
            | Q(course__tags__name__icontains=q)
        ).distinct()

    context = {
        "course": course,
        "course_comments": course_comments,
        "comment_type": comment_type,
    }
    return render(request, "courses/course_comment.html", context)


def courses(request):
    courses = Course.objects.all().order_by('-pk')

    # 검색
    search_q = request.GET.get('search-q','')
    if search_q:
        courses = courses.filter(
            Q(title__icontains=search_q)|
            Q(content__icontains=search_q)
        )

    categories = courses.values_list('category', flat=True).distinct()
    category_list = set(','.join(list(categories)).replace(', ', ',').split(','))
    selected_category = request.GET.get('category')
        
    # 선택한 태그들 가져옴
    tag_list = []
    if selected_category:
        tags = Tag.objects.filter(course__category=selected_category).distinct()
        for tag in tags:
            tag_list.append(tag.slug)
        courses = courses.filter(tags__slug__in=tag_list).distinct()

    else:
        tags = Tag.objects.all()
        
    selected_slugs = request.GET.get('tags') 

    if selected_slugs:
        selected_tags = selected_slugs.split(",")
        courses = courses.filter(tags__slug__in=selected_tags).distinct()

    # 옵션
    options = request.GET.get('option', '').split(',')
    if options:
        price_condition = Q()
        level_condition = Q()
        discount_condition = Q()
        for option in options:
            if option == '무료':
                price_condition |= Q(price=0)  
            elif option == '유료':
                price_condition |= ~Q(price=0) 
            elif option == '할인중':
                discount_condition |= ~Q(discount_rate=0)  
            elif option == '입문':
                level_condition |= Q(level='level1')  
            elif option == '초급':
                level_condition |= Q(level='level2')  
            elif option == '중급이상':
                level_condition |= Q(level='level3')  
                
        courses = courses.filter(price_condition & discount_condition & level_condition)

    # 정렬
    order = request.GET.get('sort')
    if order == 'rating':
        courses = courses.order_by('-star')
    elif order == 'enrollment':
        courses = courses.annotate(num_enrolment_users=Count('enrolment_users')).order_by('-num_enrolment_users')

    context = {
        'courses': courses,
        'tags': tags,
        'category_list': category_list,
        'selected_category': selected_category,
    }
    return render(request, "courses/course_courses.html", context)


def review_create(request, course_pk):
    if request.method == "POST":
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            course = Course.objects.get(pk=course_pk)
            review.course = course
            review.user = request.user
            review.save()
            return redirect("courses:detail", course_pk)
    else:
        review_form = ReviewForm()
    context = {
        "review_form": review_form,
    }
    return render(request, "communities/comment_create.html", context)


def review_delete(request, course_pk, review_pk):
    review = Review.objects.get(pk=review_pk)
    if request.user == review.user:
        review.delete()
        return redirect("courses:detail", course_pk)


def video(request, course_pk):
    course = Course.objects.get(pk=course_pk)
    user = request.user
    quizzes = Quiz.objects.filter(course=course)
    all_quizzes_completed = all(
        StudentAnswer.objects.filter(qna__quiz=quiz, student=user).exists()
        for quiz in quizzes
    )
    urls = Url.objects.filter(course_id=course_pk)
    context = {
        "course": course,
        "all_quizzes_completed": all_quizzes_completed,
        "urls": urls,
    }
    return render(request, "courses/course_video.html", context)


@login_required
def quiz_create(request, course_pk):
    course = Course.objects.get(pk=course_pk)
    quiz_form = QuizForm(request.POST or None)
    QnAFormSet = formset_factory(QnAForm, extra=5)
    qna_formset = QnAFormSet(request.POST or None)

    if request.method == "POST":
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
            return redirect("courses:detail", course_pk)

    context = {
        "quiz_form": quiz_form,
        "qna_formset": qna_formset,
        "course": course,
    }
    return render(request, "courses/course_quiz_create.html", context)


def quiz(request, course_pk, quiz_pk):
    quiz = Quiz.objects.get(pk=quiz_pk)
    questions = quiz.questions.all()

    if request.method == "POST":
        student = request.user
        for question in questions:
            student_answer, created = StudentAnswer.objects.get_or_create(
                qna=question, student=student
            )
            student_answer.is_correct = question.answer_text == request.POST.get(
                str(question.id)
            )
            student_answer.save()
        return redirect("courses:quiz_result", course_pk, quiz_pk)

    context = {
        "quiz": quiz,
        "questions": questions,
    }
    return render(request, "courses/course_quiz.html", context)


@login_required
def quiz_result(request, course_pk, quiz_pk):
    quiz = Quiz.objects.get(id=quiz_pk)
    total_questions = quiz.questions.count()
    student_answers = StudentAnswer.objects.filter(qna__quiz=quiz, student=request.user)
    num_correct_answers = student_answers.filter(is_correct=True).count()
    num_incorrect_answers = student_answers.filter(is_correct=False).count()
    context = {
        "quiz": quiz,
        "total_questions": total_questions,
        "num_correct_answers": num_correct_answers,
        "num_incorrect_answers": num_incorrect_answers,
    }
    return render(request, "courses/course_quiz_result.html", context)


@login_required
def enrolment(request, course_pk):
    course = Course.objects.get(pk=course_pk)
    if request.method == "POST":
        if course.enrolment_users.filter(pk=request.user.pk).exists():
            course.enrolment_users.remove(request.user)
        else:
            course.enrolment_users.add(request.user)
    else:
        pass
    return redirect("/accounts/mypage/?q=cart")

@login_required

def cart(request, course_pk):
    course = Course.objects.get(pk=course_pk)
    if request.method == "POST":
        if course.cart_users.filter(pk=request.user.pk).exists():
            course.cart_users.remove(request.user)
        else:
            course.cart_users.add(request.user)
    else:
        return redirect("/accounts/mypage/?q=cart")
    return redirect("courses:detail", course_pk)

