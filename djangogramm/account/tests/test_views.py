import pytest
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from account import views


@pytest.mark.django_db
def test_home_logged_in(client, testuser):
    client.force_login(testuser)
    url = reverse(views.home)
    resp = client.get(url)

    assert resp.status_code == 200
    assert f"Welcome to DjangoGramm, {testuser.username}!" in str(resp.content)


@pytest.mark.django_db
def test_register(client):
    url = reverse(views.register)
    resp = client.get(url)
    assert resp.status_code == 200

    form_data = {
        'username': 'testname',
        'first_name': "first",
        'last_name': "last",
        'email': "test@email.com",
        'password1': "testpassword1",
        'password2': "testpassword1"
    }

    resp = client.post(url, form_data)
    assert resp.status_code == 302
    assert resp.url == "/account/login"


@pytest.mark.django_db
def test_register_form_not_valid(client):
    form_data = {
        'username': 'testname',
        'first_name': "first",
        'last_name': "last",
        'email': "test@email.com",
        'password1': "12345",
        'password2': "12345"
    }

    url = reverse(views.register)
    resp = client.post(url, form_data)
    assert resp.status_code == 200
    assert "Wrong registration data:" in str(resp.content)


@pytest.mark.django_db
def test_view_profile(client, testuser):
    client.force_login(testuser)
    url = reverse(views.view_profile, kwargs={'pk': testuser.pk})
    resp = client.get(url)

    assert resp.status_code == 200
    assert testuser.username in str(resp.content)
    assert testuser.userprofile.bio in str(resp.content)


@pytest.mark.django_db
def test_edit_profile(client, testuser):
    client.force_login(testuser)
    url = reverse(views.edit_profile)
    resp = client.get(url)

    assert resp.status_code == 200

    newavatar = SimpleUploadedFile(name='newavatar.jpg', content=b'', content_type='image/jpeg')
    form_data = {
        'avatar': newavatar,
        'bio': 'new user1 bio',
        'first_name': 'new usr1_first_name',
        'last_name': 'new usr1_last_name',
    }

    resp = client.post(url, form_data)
    assert resp.status_code == 302
    assert resp.url == f"/account/profile/{testuser.pk}"

    url = reverse(views.view_profile, kwargs={'pk': testuser.pk})
    resp = client.get(url)
    assert 'new user1 bio' in str(resp.content)
    assert 'new usr1_first_name' in str(resp.content)
    assert 'new usr1_last_name' in str(resp.content)


@pytest.mark.django_db
def test_follow_view(client, testuser, testuser2):
    client.force_login(testuser)

    url = reverse(views.follow_view, kwargs={'pk': testuser2.pk})  # follow
    resp = client.post(url, {'profile_owner_id': testuser2.id})
    assert resp.status_code == 200
    assert resp['content-type'] == "application/json"

    url = reverse(views.view_profile, kwargs={'pk': testuser2.pk})  # check if post is followed
    resp = client.get(url)
    one_follower = "<small><strong>1</strong> followers</small>"
    assert resp.status_code == 200
    assert one_follower in str(resp.content)

    url = reverse(views.follow_view, kwargs={'pk': testuser2.pk})  # unfollow
    resp = client.post(url, {'profile_owner_id': testuser2.id})
    assert resp.status_code == 200
    assert resp['content-type'] == "application/json"

    url = reverse(views.view_profile, kwargs={'pk': testuser2.pk})  # check if post is unfollowed
    resp = client.get(url)
    no_followers = "<small><strong>0</strong> followers</small>"
    assert resp.status_code == 200
    assert no_followers in str(resp.content)