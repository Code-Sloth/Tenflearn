from django import forms
from django.forms import ClearableFileInput
from .models import Course, Review
from taggit.forms import TagField

class CoursesForm(forms.ModelForm):
    tags = TagField()
    class Meta:
        model = Course
        fields = ('title', 'content', 'price', 'discount_rate', 'image', 'expired_date', 'certificates', 'level', 'tags',)
        labels = {
                'title': '제목',
                'content': '내용',
                'star': '별점',
                'price': '금액',
                'discount_rate': '할인율',
                'discounted_price': '최종금액',
                'image': '이미지',
                'expired_date': '수강기한',
                'level': '난이도',
                'certificates': '수료증',
                'created_at': '생성일',
                'tags': '태그',
            }
        widgets = {'title': forms.TextInput(
                    attrs={
                        'class':'form-control',
                        'placeholder' : '제목을 입력해 주세요',
                }),
                'content': forms.Textarea(
                    attrs={
                        'class':'form-control',
                        'placeholder' : '내용을 입력해 주세요',
                        'style': 'border:none;'
                }),
                'image': ClearableFileInput(
                    attrs={
                        'class': 'form-control',
                        'style': 'width: 400px;'
                }),
                'expired_date': forms.DateInput(
                    attrs={'class': 'form-control', 
                        'type': 'date',  
                        'style': 'width: 400px;'
                }),
        }


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = (
            'content',
            'star',
        )
        labels = {
            'content': '',
        }
        widgets = {'content': forms.Textarea(
                    attrs={
                        'placeholder': '좋은 수강평을 남겨주시면 지식공유자와 이후 배우는 사람들에게 큰 도움이 됩니다!',
                        'cols': 100,
                        'rows': 3,
                }),
                'star': forms.NumberInput(
                    attrs={
                        'min': '1',
                        'max': '5',
                }),
        }

