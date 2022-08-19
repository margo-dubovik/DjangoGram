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

    liked = False
    if post.likes.filter(user_id=request.user.id).exists():
        liked = True

    post_images = Image.objects.filter(post_id=pk).all()
    return render(request, 'post_details.html',
                  {'post': post, 'post_images': post_images, 'liked': liked})


@login_required
def like_view(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    if post.likes.filter(user_id=request.user.id).exists():
        post.likes.remove(request.user.userprofile)
    else:
        post.likes.add(request.user.userprofile)

    return redirect(f'/post/{pk}')

