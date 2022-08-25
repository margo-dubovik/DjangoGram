import pytest
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from post.models import Post
from post import views


@pytest.mark.django_db
def test_new_post(client, testuser):
    client.force_login(testuser)

    url = reverse(views.new_post)
    resp = client.get(url)
    assert resp.status_code == 200

    img1 = SimpleUploadedFile(name='post_img1.jpg', content=b'', content_type='image/jpeg')
    img2 = SimpleUploadedFile(name='post_img2.jpg', content=b'', content_type='image/jpeg')
    images = [img1, img2]

    form_data = {
        'title': 'test post title',
        'body': 'test post body',
        'tags': 'tag1,tag2,tag3',
        'images': images,
    }

    resp = client.post(url, form_data)
    assert resp.status_code == 302
    assert resp.url == "/post/all"

    url = reverse(views.all_posts)
    resp = client.get(url)

    assert resp.status_code == 200
    assert 'test post title' in str(resp.content)
    assert 'test post body' in str(resp.content)
    all_tags = ['tag1', 'tag2', 'tag3']
    assert all(tag in str(resp.content) for tag in all_tags)


@pytest.mark.django_db
def test_all_posts(client, testuser, post1, post2):
    client.force_login(testuser)

    url = reverse(views.all_posts)
    resp = client.get(url)
    items_in = [str(post1.userprofile), post1.title, post1.body, str(post2.userprofile), post2.title, post2.body]

    assert resp.status_code == 200
    assert all(item in str(resp.content) for item in items_in)

    url = reverse(views.all_posts, kwargs={'tag_slug': 'tag1'})
    resp = client.get(url)

    assert resp.status_code == 200
    assert all(item in str(resp.content) for item in items_in)

    url = reverse(views.all_posts, kwargs={'tag_slug': 'tag2'})
    resp = client.get(url)
    items_in = [str(post1.userprofile), post1.title, post1.body, ]
    items_notin = [post2.title, post2.body]

    assert resp.status_code == 200
    assert all(item in str(resp.content) for item in items_in)
    assert all(item not in str(resp.content) for item in items_notin)


@pytest.mark.django_db
def test_post_details(client, testuser, post1):
    client.force_login(testuser)

    url = reverse(views.post_details, kwargs={'pk': post1.pk})
    resp = client.get(url)
    items_in = [str(post1.userprofile), post1.title, post1.body, ]
    print("content=", resp.content)
    assert resp.status_code == 200
    assert all(item in str(resp.content) for item in items_in)


@pytest.mark.django_db
def test_like_view(client, testuser, post1):
    client.force_login(testuser)

    url = reverse(views.like_view, kwargs={'pk': post1.pk})  # like
    resp = client.post(url, {'post_id': post1.id})
    assert resp.status_code == 302
    assert resp.url == f"/post/{post1.pk}"

    url = reverse(views.post_details, kwargs={'pk': post1.pk})  # check if post is liked
    resp = client.get(url)
    assert resp.status_code == 200
    assert "1 like(s)" in str(resp.content)

    url = reverse(views.like_view, kwargs={'pk': post1.pk})  # unlike
    resp = client.post(url, {'post_id': post1.id})
    assert resp.status_code == 302
    assert resp.url == f"/post/{post1.pk}"

    url = reverse(views.post_details, kwargs={'pk': post1.pk})  # check if post is unliked
    resp = client.get(url)
    assert resp.status_code == 200
    assert "0 like(s)" in str(resp.content)
