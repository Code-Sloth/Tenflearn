from django.shortcuts import render
from .models import Course

# Create your views here.

def index(request):
    return render(request, 'courses/course_index.html')

def detail(request, course_pk):
    course = Course.objects.get(pk=course_pk)
    context = {
        'course': course,
    }
    return render(request, 'courses/course_detail.html', context)


def comment(request):
    return render(request, 'courses/course_comment.html')


def courses(request):
    return render(request, 'courses/course_courses.html')