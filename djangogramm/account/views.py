from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.template.loader import render_to_string

from .forms import RegistrationForm


@login_required
def home(request):
    return render(request, "account/home.html", {'user': request.user})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/account/login')
        return render(request, 'account/reg_form.html', {'form': form})

    else:
        form = RegistrationForm()
        return render(request, 'account/reg_form.html', {'form': form})


@login_required
def view_profile(request, pk):
    profile_owner = get_object_or_404(User, pk=pk)
    current_user = request.user

    followed = False
    if profile_owner.id != current_user.id:
        if profile_owner.userprofile.followers.filter(id=current_user.id).exists():
            followed = True

    return render(request, 'account/profile.html',
                  {'profile_owner': profile_owner,
                   'current_user': current_user,
                   'followed': followed})


@login_required
def follow_view(request, pk):
    profile_owner = get_object_or_404(User, pk=pk)
    current_user = request.user
    if profile_owner.userprofile.followers.filter(id=current_user.id).exists():
        profile_owner.userprofile.followers.remove(current_user)
        current_user.userprofile.following.remove(profile_owner)
        followed = False
    else:
        profile_owner.userprofile.followers.add(current_user)
        current_user.userprofile.following.add(profile_owner)
        followed = True

    html = render_to_string('account/follow_section.html',
                            {'profile_owner': profile_owner,
                             'current_user': current_user,
                             'followed': followed}, request=request)
    return JsonResponse({'html': html})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        avatar = request.FILES.get('avatar')
        bio = request.POST['bio']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        profile = request.user.userprofile
        profile_owner = request.user
        if avatar:
            profile.avatar = avatar
        if bio:
            profile.bio = bio
        if email:
            profile_owner.email = email
        if first_name:
            profile_owner.first_name = first_name
        if last_name:
            profile_owner.last_name = last_name
        profile.save()
        profile_owner.save()
        return redirect(f'/account/profile/{request.user.pk}')
    else:
        return render(request, 'account/edit_profile.html', {'user': request.user})


@login_required
def all_users(request):
    users = User.objects.filter(is_staff=False)
    title = "Djangogramm users"
    return render(request, 'account/users_list.html', {'users': users, 'title': title})


@login_required
def profile_followers(request, pk):
    profile_owner = get_object_or_404(User, pk=pk)
    followers = profile_owner.userprofile.followers.all()
    title = f"{profile_owner} followers"
    return render(request, 'account/users_list.html', {'users': followers, 'title': title})


@login_required
def profile_following(request, pk):
    profile_owner = get_object_or_404(User, pk=pk)
    following = profile_owner.userprofile.following.all()
    title = f"{profile_owner} is following"
    return render(request, 'account/users_list.html', {'users': following, 'title': title})
