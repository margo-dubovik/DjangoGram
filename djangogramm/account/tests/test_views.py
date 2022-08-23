import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from account import views

@pytest.mark.django_db
def test_home_logged_in(client, django_user_model):
    # testuser = User.objects.create_user("test_user")
    username = "user1"
    password = "testpassword1"
    testuser = django_user_model.objects.create_user(username=username, password=password)
    client.login(username=username, password=password)
    url = reverse(views.home)
    resp = client.get(url)

    assert resp.status_code == 200
    assert f"Welcome to DjangoGramm, {testuser.username}!" in str(resp.content)

