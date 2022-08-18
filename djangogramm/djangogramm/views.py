from django.shortcuts import render

def home(request):
    if request.user.is_authenticated:
        return render(request, "base.html")
    else:
        return render(request, "guest_base.html")