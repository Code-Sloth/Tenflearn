from django.contrib import admin
from .models import Comment, Recomment, Review

# Register your models here.

admin.site.register(Comment)
admin.site.register(Recomment)
admin.site.register(Review)