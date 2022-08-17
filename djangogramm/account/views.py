from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required
from .models import UserProfile

# Create your views here.
def home(request):
    return render(request, "account/home.html")


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/account')
        return render(request, 'account/reg_form.html', {'form': form})

    else:
        form = RegistrationForm()

        args = {'form': form}
        return render(request, 'account/reg_form.html', args)

@login_required
def view_profile(request):
    args = {'user': request.user}
    return render(request, 'account/profile.html', args)