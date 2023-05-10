from django.db import models
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from datetime import timedelta,datetime

# Create your models here.

class Course(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    enrolment_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='enrolment_courses')
    title = models.CharField(max_length=100)
    content = models.TextField()
    star = models.DecimalField(default=0, max_digits=5, decimal_places=1)
    price = models.IntegerField(default=0)
    discount_rate = models.IntegerField(default=0)
    discounted_price = models.IntegerField()

    def course_image_path(instance, filename):
        return f'courses/{instance.title}/{filename}'

    image = ProcessedImageField(
        upload_to=course_image_path,
        processors=[ResizeToFill(100,100)],
        format='JPEG',
        options={'quality' : 100},
        blank=True,
        null=True,
    )

    expired_date = models.DateField()
    level_Choices = (('level1','입문'),('level2','초급'),('level3','중급이상'))
    level = models.CharField(max_length=20, choices=level_Choices)
    certificates = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_discount_price(self):
        return round((self.price * (1 - self.discount_rate / 100)) / 10) * 10

    def save(self,*args, **kargs):
        self.discounted_price = self.calculate_discount_price()
        super().save(*args, **kargs)
