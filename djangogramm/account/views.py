from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required
from .models import UserProfile


# Create your views here.
@login_required
def home(request):
    args = {'user': request.user}
    return render(request, "account/home.html", args)


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
def view_profile(request):
    args = {'user': request.user}
    return render(request, 'account/profile.html', args)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        avatar = request.FILES.get('avatar')
        bio = request.POST['bio']
        profile = request.user.userprofile
        profile.avatar = avatar
        profile.bio = bio
        profile.save()
        return redirect('/account/profile')
    else:
        return render(request, 'account/edit_profile.html')
