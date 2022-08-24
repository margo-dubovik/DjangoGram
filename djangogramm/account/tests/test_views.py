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
    url = reverse(views.view_profile)
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
    }

    resp = client.post(url, form_data)
    assert resp.status_code == 302
    assert resp.url == "/account/profile"

    url = reverse(views.view_profile)
    resp = client.get(url)
    assert 'new user1 bio' in str(resp.content)