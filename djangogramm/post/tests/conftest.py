import pytest

from post.models import Post


@pytest.fixture
def testuser(db, django_user_model):
    username = "user1"
    password = "testpassword1"
    user = django_user_model.objects.create_user(username=username, password=password)
    user.userprofile.bio = "user1 bio"
    user.userprofile.save()
    return user


@pytest.fixture
def post1(db, testuser):
    post1 = Post(
        userprofile=testuser.userprofile,
        title="post1",
        body="post1 body",
    )
    post1.save()

    post1_tags = ['tag1', 'tag2']
    for tag in post1_tags:
        post1.tags.add(tag)

    return post1 \
 \
 \
@pytest.fixture
def post2(db, testuser):
    post2 = Post(
        userprofile=testuser.userprofile,
        title="post2",
        body="post2 body",
    )

    post2.save()

    post2_tags = ['tag1']

    for tag in post2_tags:
        post2.tags.add(tag)

    return post2
