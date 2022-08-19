from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .forms import PostForm
from .models import Post, Image


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
            return redirect("/")
        else:
            print(postForm.errors)
    else:
        postForm = PostForm()
    return render(request, 'new_post.html', {'form': postForm})

@login_required
def all_posts(request):
    post_list = Post.objects.all()
    return render(request, 'all_posts.html', {'post_list': post_list})

@login_required
def post_details(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post_images = Image.objects.filter(post_id=pk).all()
    return render(request, 'post_details.html', {'post': post, 'post_images': post_images})


@login_required
def like_view(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    post.likes.add(request.user.userprofile)
    return redirect(f'/post/{pk}')

