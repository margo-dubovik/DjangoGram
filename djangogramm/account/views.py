from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

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
    profile_owner = get_object_or_404(User, id=request.POST.get('profile_owner_id'))
    current_user = request.user
    if profile_owner.userprofile.followers.filter(id=current_user.id).exists():
        profile_owner.userprofile.followers.remove(request.user)
    else:
        profile_owner.userprofile.followers.add(request.user)

    return redirect(f'/account/profile/{pk}')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        avatar = request.FILES.get('avatar')
        bio = request.POST['bio']
        profile = request.user.userprofile
        if avatar:
            profile.avatar = avatar
        if bio:
            profile.bio = bio
        profile.save()
        return redirect(f'/account/profile/{request.user.pk}')
    else:
        return render(request, 'account/edit_profile.html')
