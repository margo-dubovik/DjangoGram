from django.test import TestCase
import pytest

from django.contrib.auth.models import User
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile

from account.models import UserProfile

@pytest.mark.django_db
def test_userprofile_str():
    testuser = User.objects.create_user("test_user")
    userprofile = UserProfile(user=testuser, bio="some bio")
    assert str(userprofile) == "test_user"

@pytest.mark.django_db
def test_userprofile_avatar_url_default():
    testuser = User.objects.create_user("test_user")
    userprofile = UserProfile(user=testuser, bio="some bio")
    assert userprofile.avatar_url == f"{settings.MEDIA_URL}/profile_image/default_profile_img.jpg"

@pytest.mark.django_db
def test_userprofile_avatar_url():
    testuser = User.objects.create_user("test_user")
    userprofile = UserProfile(user=testuser, bio="some bio")
    userprofile.avatar = SimpleUploadedFile(name='testavatar.jpg', content=b'', content_type='image/jpeg')
    assert userprofile.avatar_url == f"{settings.MEDIA_URL}testavatar.jpg"
