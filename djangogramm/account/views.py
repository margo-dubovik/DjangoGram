from django.shortcuts import render


# Create your views here.
def users_list(request):
    return render(request, "account/users_list.html")
