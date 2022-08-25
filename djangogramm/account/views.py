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
    return render(request, 'account/profile.html',
                  {'profile_owner': profile_owner,
                   'current_user': current_user})


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
        return redirect('/account/profile')
    else:
        return render(request, 'account/edit_profile.html')
