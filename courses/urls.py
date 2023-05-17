from django.urls import path, include
from . import views


app_name = 'courses'
urlpatterns = [
    path('', views.index, name='index'),
    path('courses/', views.courses, name='courses'),
    path('course/create/', views.create, name='create'),
    path('course/<int:course_pk>/', views.detail, name='detail'),
    path('course/<int:course_pk>/update/', views.update, name='update'),
    path('course/<int:course_pk>/delete/', views.delete, name='delete'),
    path('course/<int:course_pk>/community/', views.comment, name='comment'),
    path('course/<int:course_pk>/video/', views.video, name='video'),
    path('course/<int:course_pk>/quiz/<int:quiz_pk>/', views.quiz, name='quiz'),
    path('course/<int:course_pk>/quiz/create/', views.quiz_create, name='quiz_create'),
    path('course/<int:course_pk>/quiz/<int:quiz_pk>/result/', views.quiz_result, name='quiz_result'),
    path('course/<int:course_pk>/enrolment/', views.enrolment, name='enrolment'),
    path('course/<int:course_pk>/cart/', views.cart, name="cart"),
    path('reviews/<int:course_pk>/create/', views.review_create, name='review_create'),
    path('reviews/<int:course_pk>/delete/<int:review_pk>/', views.review_delete, name='review_delete'),
]