from django.db import models
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from datetime import timedelta,datetime
from taggit.managers import TaggableManager

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
        return f'courses/{instance.pk}/{filename}'

    image = ProcessedImageField(
        upload_to=course_image_path,
        processors=[ResizeToFill(473,308)],
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
    tags = TaggableManager()

    def star_multiple(self):
        return self.star*20

    def calculate_discount_price(self):
        return round((self.price * (1 - self.discount_rate / 100)) / 10) * 10

    def save(self,*args, **kargs):
        self.discounted_price = self.calculate_discount_price()
        super().save(*args, **kargs)


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
    content = models.TextField()
    star = models.IntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def created_time(self):
        time = datetime.now(tz=timezone.utc) - self.created_at

        if time < timedelta(minutes=1):
            return '방금 전'
        elif time < timedelta(hours=1):
            return str(int(time.seconds / 60)) + '분 전'
        elif time < timedelta(days=1):
            return str(int(time.seconds / 3600)) + '시간 전'
        elif time < timedelta(days=7):
            time = datetime.now(tz=timezone.utc).date() - self.created_at.date()
            return str(time.days) + '일 전'
        else:
            return self.strftime('%Y-%m-%d')

    def save(self, *args, **kwargs):                  
        self.course.star = (self.course.star * self.course.reviews.count() + self.star) / (self.course.reviews.count() + 1)
        self.course.save()
        super(Review, self).save(*args, **kwargs)

    def delete(self, *args, **kargs):
        if self.course.reviews.count() >= 2:
            self.course.star = (self.course.star * self.course.reviews.count() - self.star) / (self.course.reviews.count() - 1)
        else:
            self.course.star = 0
        self.course.save()
        super(Review, self).delete(*args, **kargs)

    def star_multiple(self):
        return self.star*20