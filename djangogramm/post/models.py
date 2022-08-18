from django.db import models
from account.models import UserProfile
from django.template.defaultfilters import slugify


class Post(models.Model):
    userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    body = models.TextField(max_length=400)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


def get_image_filename(instance, filename):
    title = instance.post.title
    slug = slugify(title)
    return f"post_images/{slug}-{filename}"


class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_image_filename)
