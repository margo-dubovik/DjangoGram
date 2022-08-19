from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .forms import PostForm
from .models import Image


@login_required
def new_post(request):
    if request.method == 'POST':
        postForm = PostForm(request.POST)
        images = request.FILES.getlist('images')

        if postForm.is_valid():
            post_form = postForm.save(commit=False)
            post_form.userprofile = request.user.userprofile
            post_form.save()

            for image in images:
                photo = Image(post=post_form, image=image)
                photo.save()
            return HttpResponseRedirect("/")
        else:
            print(postForm.errors)
    else:
        postForm = PostForm()
    return render(request, 'new_post.html', {'form': postForm})