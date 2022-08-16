from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm


# Create your views here.
def users_list(request):
    return render(request, "account/users_list.html")


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/account')
        return render(request, 'account/reg_form.html', {'form': form})

    else:
        form = UserCreationForm

        args = {'form': form}
        return render(request, 'account/reg_form.html', args)