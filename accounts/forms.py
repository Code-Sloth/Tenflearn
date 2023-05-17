from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm, PasswordChangeForm

class CustomAutentication(AuthenticationForm):
    username = forms.CharField(
        label = False,
        widget= forms.TextInput(attrs = {
            'class':'form-control',
            "placeholder": "아이디",
            "style": "height: 47px;",
            "autocomplete": "username",
            }),
    )
    password = forms.CharField(
        label = False,
        widget = forms.PasswordInput(attrs = {
            'class':'form-control',
            "placeholder": "비밀번호",
            "style": "height: 47px;",
            "autocomplete": "current-password",
            }),
    )

    class Meta:
        model = get_user_model
        fields = ('username', 'password')

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label="아이디",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "아이디",
                "style": "height: 47px;",
            }),
    )

    last_name = forms.CharField(
        label = "성",
        widget = forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "홍",
                "style": "height: 47px;",
            }),
    )

    first_name = forms.CharField(
        label = "이름",
        widget = forms.TextInput(
            attrs = {
                "class": "form-control",
                "placeholder": "길동",
                "style": "height: 47px;",
            }),
    )

    password1 = forms.CharField(
        label="비밀번호",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "******",
                "style": "height: 47px;",
            }),
    )
    password2 = forms.CharField(
        label="비밀번호 확인",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "******",
                "style": "height: 47px;",
            }),
    )
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'last_name', 'first_name',  'password1', 'password2', 'image',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['image'].widget.attrs['class'] = 'form-control'

class CustomUserChangeForm(UserChangeForm):
    last_name = forms.CharField(
        label = "성",
        widget = forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "홍",
                "style": "height: 47px;",
            }),
    )

    first_name = forms.CharField(
        label = "이름",
        widget = forms.TextInput(
            attrs = {
                "class": "form-control",
                "placeholder": "길동",
                "style": "height: 47px;",
            }),
    )
    password = None
    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = ('last_name', 'first_name', 'image')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['image'].widget.attrs['class'] = 'form-control'


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label='기존 비밀번호',
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "기존 비밀번호",
                "style": "height: 47px;",
            }
        ),
    )
    new_password1 = forms.CharField(
        label="새 비밀번호",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "새 비밀번호",
                "style": "height: 47px;",
            }
        ),
        help_text="",
    )
    new_password2 = forms.CharField(
        label="새 비밀번호 확인",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "새 비밀번호 확인",
                "style": "height: 47px;",
            }
        ),
        help_text="",
    )