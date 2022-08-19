from django.contrib import admin
from .models import Post, Image, Tag

# Register your models here.
admin.site.register(Post)
admin.site.register(Image)
admin.site.register(Tag)