from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.conf import settings


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500)
    avatar = models.ImageField(upload_to='profile_image', blank=True)
    followers = models.ManyToManyField(User, related_name='followers')
    following = models.ManyToManyField(User, related_name='following')

    def __str__(self):
        return self.user.username

    def total_followers(self):
        return self.followers.count()

    def total_following(self):
        return self.following.count()

    @property
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        else:
            return f"{settings.MEDIA_URL}profile_image/default_profile_img.jpg"


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


post_save.connect(create_user_profile, sender=User)
