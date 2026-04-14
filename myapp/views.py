from django.shortcuts import get_object_or_404, render,redirect
from . models import Category,Post,PostImage
from . forms import PostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator

def home(request):
    posts=Post.objects.all().order_by('-id')[:8]
    return render(request,'home.html',{'posts':posts})

def article(request):
    post_list = Post.objects.all().order_by('-id')

    paginator = Paginator(post_list, 8)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    return render(request, 'article.html', {'posts': posts}) 

def post_detail(request,slug):
    post=get_object_or_404(Post,slug=slug)
    # related_posts = Post.objects.filter(category=post.category).exclude(id=post.id)[:4]
    related_posts = Post.objects.filter(category=post.category).exclude(id=post.id)[:4]
    return  render(request,'post_detail.html',{'post':post,'related_posts':related_posts})

@login_required
def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()

            images = request.FILES.getlist('image')
            if images:
                for img in images:
                    PostImage.objects.create(post=post, image=img)

            return redirect('dashboard')

    else:
        form = PostForm() 

    return render(request, 'post_form.html', {'form': form})

@login_required
def edit_post(request, id):
    post = get_object_or_404(Post, id=id, user=request.user)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)

        if form.is_valid():
            form.save()

            images = request.FILES.getlist('image')

            if images:
                post.postimage_set.all().delete()  
                for img in images:
                    PostImage.objects.create(post=post, image=img)

            return redirect('dashboard')
        else:
            print(form.errors)

    else:
        form = PostForm(instance=post)

    return render(request, 'post_form.html', {'form': form, 'post': post})

@login_required
def delete_post(request, id):
    # post = get_object_or_404(Post, id=id)
    post = get_object_or_404(Post, id=id, user=request.user)
    post.delete()
    return redirect('dashboard')



@login_required
def dashboard(request):
    posts = Post.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'posts': posts})

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        User.objects.create_user(username=username, password=password)
        return redirect('login')

    return render(request, 'register.html')


# LOGIN
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')


# LOGOUT
def logout_view(request):
    logout(request)
    return redirect('login')
