import pytest

@pytest.fixture()
def testuser(db, django_user_model):
    username = "user1"
    password = "testpassword1"
    user = django_user_model.objects.create_user(username=username, password=password)
    user.userprofile.bio = "user1 bio"
    user.userprofile.save()
    return user
