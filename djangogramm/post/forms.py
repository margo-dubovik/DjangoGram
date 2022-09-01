from django import forms
from .models import Post, Image
from taggit.forms import TagField


class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=128)
    body = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': "5"}))
    tags = TagField(label="Tags (comma-separated, no spaces):")

    class Meta:
        model = Post
        fields = ('title', 'body', 'tags')