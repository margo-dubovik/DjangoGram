from django.db import models
from account.models import UserProfile
from django.template.defaultfilters import slugify


class Tag(models.Model):
    name = models.CharField(max_length=250)


class Post(models.Model):
    userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    body = models.TextField(max_length=400)
    date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(UserProfile, related_name='liked_posts')
    tags = models.ManyToManyField(Tag, related_name='post_tags')

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()

    @property
    def post_images(self):
        return Image.objects.filter(post_id=self.pk).all()


def get_image_filename(instance, filename):
    title = instance.post.title
    slug = slugify(title)
    return f"post_images/{slug}-{filename}"


class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_image_filename)
