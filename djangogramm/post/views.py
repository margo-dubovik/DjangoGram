from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .forms import PostForm
from .models import Post, Image

from taggit.models import Tag


@login_required
def new_post(request):
    if request.method == 'POST':
        postForm = PostForm(request.POST)
        images = request.FILES.getlist('images')

        if postForm.is_valid():
            title = postForm.cleaned_data['title']
            body = postForm.cleaned_data['body']
            tags = postForm.cleaned_data['tags']
            newpost = Post(title=title, body=body)
            newpost.userprofile = request.user.userprofile
            newpost.save()
            for tag in tags:
                newpost.tags.add(tag)

            for image in images:
                photo = Image(post=newpost, image=image)
                photo.save()
            return redirect("/post/all")
        else:
            print(postForm.errors)
    else:
        postForm = PostForm()
    return render(request, 'new_post.html', {'form': postForm})

@login_required
def all_posts(request, tag_slug=None):
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = Post.objects.filter(tags__in=[tag])
    else:
        post_list = Post.objects.all()
    return render(request, 'all_posts.html', {'post_list': post_list, 'tag': tag})

@login_required
def post_details(request, pk):
    post = get_object_or_404(Post, pk=pk)

    liked = False
    if post.likes.filter(user_id=request.user.id).exists():
        liked = True

    return render(request, 'post_details.html',
                  {'post': post, 'liked': liked})


@login_required
def like_view(request, pk):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        print("Yes, AJAX!")
    else:
        print("not AJAX")
        post = get_object_or_404(Post, id=request.POST.get('post_id'))
        if post.likes.filter(user_id=request.user.id).exists():
            post.likes.remove(request.user.userprofile)
        else:
            post.likes.add(request.user.userprofile)

        return redirect(f'/post/{pk}')

