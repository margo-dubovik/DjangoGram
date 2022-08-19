from django.urls import path
from . import views

urlpatterns = [
    path('new/', views.new_post),
    path('all/', views.all_posts),
    path('<int:pk>', views.post_details, name='post-details')
    ]
