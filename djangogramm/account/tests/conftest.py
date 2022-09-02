import pytest


@pytest.fixture
def testuser(db, django_user_model):
    username = "user1"
    password = "testpassword1"
    user = django_user_model.objects.create_user(username=username, password=password)
    user.userprofile.bio = "user1 bio"
    user.email = "user1_email@gmail.com"
    user.userprofile.save()
    return user


@pytest.fixture
def testuser2(db, django_user_model):
    username = "user2"
    password = "testpassword2"
    user = django_user_model.objects.create_user(username=username, password=password)
    user.userprofile.bio = "user2 bio"
    user.email = "user2_email@gmail.com"
    user.userprofile.save()
    return user
