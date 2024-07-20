from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import ListView

from .forms import UserRegistrationForm, CommentForm
from .models import Profile, Blog, Comment, Profile


class IndexView(View):
    def get(self, request):
        return render(request, 'blog_app/index.html')


class RegistrationView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('blog_app:index')
        user_form = UserRegistrationForm()
        context = {
            'user_form': user_form
        }
        return render(request, 'blog_app/register.html', context=context)

    def post(self, request):
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            phone_number = user_form.cleaned_data.get('phone_number')
            profile_photo = user_form.cleaned_data.get('profile_photo')
            bio = user_form.cleaned_data.get('bio')
            Profile.objects.create(user=user, phone_number=phone_number, profile_photo=profile_photo, bio=bio)
            username = user_form.cleaned_data.get('username')
            password = user_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('blog_app:index')
        else:
            context = {
                'user_form': user_form
            }
            return render(request, 'blog_app/register.html', context=context)


class MyLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'blog_app/login.html'

    def get_success_url(self):
        messages.success(self.request, 'You logged in successfully')
        return reverse_lazy('blog_app:index')

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid credentials')
        return self.render_to_response(self.get_context_data(form=form))


class AllBlogsView(View):
    def get(self, request):
        blogs = Blog.objects.order_by('-publication_date').select_related('blogger')
        paginator = Paginator(blogs, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'page_obj': page_obj
        }
        return render(request, 'blog_app/all_blogs.html', context=context)


class BlogView(View):
    def get(self, request, pk, blogger_pk=None):
        blog = Blog.objects.get(pk=pk)
        comments = Comment.objects.order_by('-publication_date').filter(blog_id=pk)
        context = {
            'blog': blog,
            'comments': comments,
        }
        if blogger_pk:
            blogger = User.objects.get(pk=blogger_pk)
            context['blogger'] = blogger
        return render(request, 'blog_app/blog.html', context=context)


class BloggerView(View):
    def get(self, request, pk):
        blogger = Profile.objects.get(pk=pk)
        blogs = Blog.objects.order_by('-publication_date').filter(blogger_id=pk)
        context = {
            'blogger': blogger,
            'blogs': blogs,
        }
        return render(request, 'blog_app/blogger.html', context=context)


class CommentView(LoginRequiredMixin, View):
    def get(self, request, pk):
        form = CommentForm()
        context = {
            'form': form,
            'pk': pk,
        }
        return render(request, 'blog_app/comment.html', context=context)

    def post(self, request, pk):
        form = CommentForm(request.POST)
        context = {
            'form': form,
        }
        if form.is_valid():
            kwargs = {
                'user': request.user,
                'blog': Blog.objects.get(pk=pk),
                'description': form.cleaned_data.get('description')
            }
            Comment.objects.create(**kwargs)
            return redirect('blog_app:blog', pk)

        return render(request, 'blog_app/comment.html', context=context)


class BloggerListView(ListView):
    model = Profile
    template_name = 'blog_app/bloggers.html'
    context_object_name = 'bloggers'
    paginate_by = 5
