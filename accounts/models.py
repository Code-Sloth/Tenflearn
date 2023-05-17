from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.conf import settings
import os
from django.contrib.auth.models import User
from courses.models import Course

# Create your models here.

class User(AbstractUser):
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')

    position_Choices = (('tutor','강사'),('student','학생'))
    position = models.CharField(max_length=20, choices=position_Choices)

    def profile_image_path(instance, filename):
        return f'accounts/{instance.pk}/{filename}'

    image = ProcessedImageField(
        upload_to=profile_image_path,
        processors=[ResizeToFill(300,300)],
        format='JPEG',
        options={'quality' : 100},
        blank=True,
        null=True,
    )

    def delete(self, *args, **kargs):
        if self.image:
            os.remove(os.path.join(settings.MEDIA_ROOT, self.image.path))
            dir_path = os.path.dirname(os.path.join(settings.MEDIA_ROOT, self.image.name))
            if not os.listdir(dir_path):
                os.rmdir(dir_path)
        super(User, self).delete(*args, **kargs)

    def save(self, *args, **kwargs):
        if self.id:
            old_user = User.objects.get(id=self.id)
            if self.image != old_user.image:
                if old_user.image:
                    os.remove(os.path.join(settings.MEDIA_ROOT, old_user.image.path))
        super(User, self).save(*args, **kwargs)