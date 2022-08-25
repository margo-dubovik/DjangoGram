from django.urls import path
from . import views

urlpatterns = [
    path('new/', views.new_post, name='new-post'),
    path('all/', views.all_posts, name='all-posts'),
    path('<int:pk>', views.post_details, name='post-details'),
    path('like/<int:pk>', views.like_view, name='like_post'),
    path('tag/<slug:tag_slug>', views.all_posts, name='post_tag'),
    ]
