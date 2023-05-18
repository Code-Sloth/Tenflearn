from django.contrib import admin
from .models import Course, Review, Url, Quiz, StudentAnswer

# Register your models here.

admin.site.register(Course)
admin.site.register(Review)
admin.site.register(Url)
admin.site.register(Quiz)
admin.site.register(StudentAnswer)
