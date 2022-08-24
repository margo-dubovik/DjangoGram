from django import forms
from .models import Post, Image
from taggit.forms import TagField


class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=128)
    body = forms.CharField(max_length=500)
    tags = TagField(label="Tags (comma-separated, no spaces):")

    class Meta:
        model = Post
        fields = ('title', 'body', 'tags')