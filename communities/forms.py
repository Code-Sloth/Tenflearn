from django import forms
from .models import Comment, Recomment
from ckeditor.widgets import CKEditorWidget


class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Comment
        fields = (
            "title",
            "category",
            "content",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs["class"] = "form-control"
        self.fields["title"].widget.attrs["placeholder"] = "제목"
        self.fields["category"].widget.attrs["class"] = "form-control"
        self.fields["category"].widget.attrs["placeholder"] = "카테고리"
        self.fields["content"].widget.attrs["class"] = "form-control"


class RecommentForm(forms.ModelForm):
    class Meta:
        model = Recomment
        fields = ("content",)
