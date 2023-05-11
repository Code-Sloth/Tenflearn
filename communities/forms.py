from django import forms
from .models import Comment, Recomment
from ckeditor.widgets import CKEditorWidget

class CommentForm(forms.ModelForm):
    content = forms.CharField(
        widget=CKEditorWidget()
        )
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
        fields = (
            'content',
        )

