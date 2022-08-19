from django import forms
from .models import Post, Image


class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=128)
    body = forms.CharField(max_length=245)

    class Meta:
        model = Post
        fields = ('title', 'body',)