from django.urls import path, include
from . import views


app_name = 'courses'
urlpatterns = [
    path('', views.index, name='index'),
    path('courses/', views.courses, name='courses'),
    path('course/<int:course_pk>/', views.detail, name='detail'),
    path('course/<int:course_pk>/community/', views.comment, name='comment'),
]