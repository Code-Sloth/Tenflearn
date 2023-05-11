from django import forms
from .models import Course, Review

class CoursesForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('__all__')
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
            }
        widgets = {
        }


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = (
            'content',
            'star',
        )
