import pytest

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile

from post.models import Post, Image

@pytest.mark.django_db
def test_userprofile_str(testuser):
    post = Post(
        userprofile=testuser.userprofile,
        title="test title",
        body="test_body",
                )
    assert str(post) == "test title"