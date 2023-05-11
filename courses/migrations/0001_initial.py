# Generated by Django 3.2.18 on 2023-05-11 08:06

import courses.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import imagekit.models.fields
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taggit', '0005_auto_20220424_2025'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('star', models.DecimalField(decimal_places=1, default=0, max_digits=5)),
                ('price', models.IntegerField(default=0)),
                ('discount_rate', models.IntegerField(default=0)),
                ('discounted_price', models.IntegerField()),
                ('image', imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to=courses.models.Course.course_image_path)),
                ('expired_date', models.DateField()),
                ('level', models.CharField(choices=[('level1', '입문'), ('level2', '초급'), ('level3', '중급이상')], max_length=20)),
                ('certificates', models.BooleanField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('enrolment_users', models.ManyToManyField(related_name='enrolment_courses', to=settings.AUTH_USER_MODEL)),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('star', models.IntegerField(default=5, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='courses.course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
