from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import RegistrationForm

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