import pytest
from django.urls import reverse
from account import views

@pytest.mark.django_db
def test_home_logged_in(client, django_user_model):
    username = "user1"
    password = "testpassword1"
    testuser = django_user_model.objects.create_user(username=username, password=password)
    client.login(username=username, password=password)
    url = reverse(views.home)
    resp = client.get(url)

    assert resp.status_code == 200
    assert f"Welcome to DjangoGramm, {testuser.username}!" in str(resp.content)


@pytest.mark.django_db
def test_register(client, django_user_model):
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
def test_register_form_not_valid(client, django_user_model):
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