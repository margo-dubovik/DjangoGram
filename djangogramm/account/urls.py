from django.urls import path, include
from . import views
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('', views.home),
    path('register/', views.register),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('login/', LoginView.as_view(template_name='account/login.html'), name="login"),
    path('logout/', LogoutView.as_view(template_name='account/logout.html'), name="logout"),
    path('profile/<int:pk>', views.view_profile, name="view-profile"),
    path('follow/<int:pk>', views.follow_view, name='follow-user'),
    path('profile/edit', views.edit_profile, name="edit-profile"),
    path('all/', views.all_users, name="all-users"),
    path('profile/<int:pk>/followers', views.profile_followers, name="profile-followers"),
    path('profile/<int:pk>/following', views.profile_following, name="profile-following"),
    ]