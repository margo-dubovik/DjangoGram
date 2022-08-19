from django.shortcuts import render
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from .forms import ImageForm, PostForm
from .models import Image

# Create your views here.
@login_required
def post(request):
    ImageFormSet = modelformset_factory(Image, form=ImageForm, extra=3)
    if request.method == 'POST':

        postForm = PostForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES,
                               queryset=Image.objects.none())

        if postForm.is_valid() and formset.is_valid():
            post_form = postForm.save(commit=False)
            post_form.userprofile = request.user.userprofile
            post_form.save()

            for form in formset.cleaned_data:
                if form:
                    image = form['image']
                    photo = Image(post=post_form, image=image)
                    photo.save()
            messages.success(request,
                             "Post created successfully!")
            return HttpResponseRedirect("/")
        else:
            print(postForm.errors, formset.errors)
    else:
        postForm = PostForm()
        formset = ImageFormSet(queryset=Image.objects.none())
    return render(request, 'post_creation.html',
                  {'form': postForm, 'formset': formset})