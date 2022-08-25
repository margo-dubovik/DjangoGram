import pytest

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile

from account.models import UserProfile
from dotenv import load_dotenv
import os
load_dotenv()

@pytest.mark.django_db
def test_userprofile_str(django_user_model):
    testuser = django_user_model.objects.create_user("test_user")
    userprofile = UserProfile(user=testuser, bio="some bio")
    assert str(userprofile) == "test_user"

@pytest.mark.django_db
def test_userprofile_avatar_url_default(django_user_model):
    testuser = django_user_model.objects.create_user("test_user")
    userprofile = UserProfile(user=testuser, bio="some bio")
    assert userprofile.avatar_url == f"{settings.MEDIA_URL}profile_image/default_profile_img.jpg"

@pytest.mark.django_db
def test_userprofile_avatar_url(django_user_model):
    testuser = django_user_model.objects.create_user("test_user")
    userprofile = UserProfile(user=testuser, bio="some bio")
    userprofile.avatar = SimpleUploadedFile(name='testavatar.jpg', content=b'', content_type='image/jpeg')
    assert userprofile.avatar_url == f"https://{os.environ.get('MY_AWS_STORAGE_BUCKET_NAME')}.s3.amazonaws.com" \
                                     f"/testavatar.jpg"
