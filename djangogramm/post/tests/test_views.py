import pytest
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

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


