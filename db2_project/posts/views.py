from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.http import JsonResponse
from .forms import SignUpForm, CommentForm
from .tokens import account_activation_token
from .models import Post
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)

            return redirect('account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def account_activation_sent(request):
    return render(request, 'account_activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'account_activation_invalid.html')


@login_required
def index(request, order_by='asc'):
    if order_by == 'desc':
        post_list = Post.objects.all().order_by('-title')
        reverse_order = 'asc'
    else:
        post_list = Post.objects.all().order_by('title')
        reverse_order = 'desc'
    page = request.GET.get('page', 1)
    paginator = Paginator(post_list, 2)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    if request.GET.get('search_box'):
        query = request.GET.get('search_box')
        if query:
            posts = Post.objects.filter(
                Q(title__contains=query)|
                Q(body__contains=query)|
                Q(description__contains=query)
            )

    liked_post = request.user.post_likes.all()

    return render(request, 'post_list.html', {'posts': posts, 'liked_post': liked_post, 'order': order_by,
                                              'reverse': reverse_order})


@login_required
def detail(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        raise Http404("Question does not exist")
    comment_list = post.comments.all().order_by('-created_date')
    page = request.GET.get('page', 1)

    paginator = Paginator(comment_list, 2)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)
    return render(request, 'detail.html', {'post': post, 'comments': comments})


@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('detail', post_id=post.pk)
    else:
        form = CommentForm()
    return render(request, 'add_comment_to_post.html', {'form': form})


def add_like(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.likes.add(request.user)
    return JsonResponse({'likes': post.likes.count()})


def remove_like(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.likes.remove(request.user)
    return JsonResponse({'likes': post.likes.count()})

