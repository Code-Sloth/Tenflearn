from django import forms
from .models import Review, Comment, Recomment

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = (
            'title',
            'category',
            'content',
        )

class RecommentForm(forms.ModelForm):

    class Meta:
        model = Recomment
        field = (
            'content'
        )


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = (
            'content',
            'star',
        )
