from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.views.generic import ListView
from django.contrib.auth import logout

from .forms import UserRegistrationForm, CommentForm, ProfileEditForm, BlogEditForm
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
        return self.request.GET.get('next', reverse_lazy('blog_app:index'))

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
        blogger = Profile.objects.get(user_id=pk)
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


# class BloggerListView(ListView):
#     model = Blog
#     template_name = 'blog_app/bloggers.html'
#     context_object_name = 'blogs'
#     paginate_by = 5


class BloggerListView(View):
    def get(self, request):
        # bloggers = Blog.objects.all().values('blogger').distinct()
        blogs = Blog.objects.all().select_related('blogger')
        bloggers = list()
        for blog in blogs:
            user = User.objects.get(pk=blog.blogger_id)
            if user not in bloggers:
                bloggers.append(user)

        paginator = Paginator(bloggers, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'bloggers': page_obj,
        }
        return render(request, 'blog_app/bloggers.html', context=context)


def show_base_template_view(request):
    return render(request, 'blog_app/base.html')


class MyProfileView(LoginRequiredMixin, View):
    def get(self, request):
        profile = Profile.objects.get(user_id=request.user.pk)
        blogs = Blog.objects.filter(blogger_id=request.user.pk).all()
        context = {
            'profile': profile,
            'blogs': blogs,
        }
        return render(request, 'blog_app/my_profile.html', context=context)


class ProfileEditView(LoginRequiredMixin, View):
    def get(self, request):
        first_name = request.user.first_name
        last_name = request.user.last_name

        profile = Profile.objects.get(user_id=request.user.pk)
        phone_number = profile.phone_number
        bio = profile.bio

        user_kwargs = {
            'first_name': first_name,
            'last_name': last_name,
            'phone_number': phone_number,
            'bio': bio,
        }
        form = ProfileEditForm(initial={**user_kwargs})
        context = {
            'form': form,
        }
        return render(request, 'blog_app/edit_profile.html', context=context)

    def post(self, request):
        form = ProfileEditForm(request.POST, request.FILES)
        context = {
            'form': form,
        }
        if form.is_valid():
            user_kwargs = {
                'first_name': form.cleaned_data.get('first_name'),
                'last_name': form.cleaned_data.get('last_name'),
            }

            profile_kwargs = {
                'phone_number': form.cleaned_data.get('phone_number'),
                'bio': form.cleaned_data.get('bio'),
            }

            if form.cleaned_data.get('profile_photo'):
                profile = Profile.objects.get(user_id=request.user.pk)
                profile.profile_photo = form.cleaned_data.get('profile_photo')
                profile.save()

            User.objects.filter(pk=request.user.pk).update(**user_kwargs)
            Profile.objects.filter(user_id=request.user.pk).update(**profile_kwargs)
            return redirect('blog_app:profile')

        return render(request, 'blog_app/edit_profile.html', context=context)


class BlogEditView(View):
    def get(self, request, pk):
        blog = Blog.objects.get(pk=pk)

        if blog.blogger_id != request.user.pk:
            raise PermissionDenied()

        form = BlogEditForm(initial={'name': blog.name, 'content': blog.content})
        context = {
            'form': form,
            'pk': pk,
        }

        return render(request, 'blog_app/edit_blog.html', context=context)

    def post(self, request, pk):
        form = BlogEditForm(request.POST)
        context = {
            'form': form,
        }

        if form.is_valid():
            kwargs = {
                'name': form.cleaned_data.get('name'),
                'content': form.cleaned_data.get('content'),
            }
            Blog.objects.filter(pk=pk).update(**kwargs)
            return redirect('blog_app:blog', *(pk, request.user.pk))

        return render(request, 'blog_app/edit_blog.html', context=context)


class DeleteBlogView(View):
    def post(self, request, pk):
        blog = Blog.objects.filter(pk=pk)
        context = {
            'blog': blog,
        }
        blog.delete()
        return render(request, 'blog_app/deleted.html', context=context)


class AddBlogView(View):
    def get(self, request):
        form = BlogEditForm()
        context = {
            'form': form,
        }
        return render(request, 'blog_app/add_blog.html', context=context)

    def post(self, request):
        form = BlogEditForm(request.POST)
        context = {
            'form': form,
        }
        if form.is_valid():
            kwargs = {
                'name': form.cleaned_data.get('name'),
                'content': form.cleaned_data.get('content'),
                'blogger': request.user
            }
            blog = Blog.objects.create(**kwargs)
            return redirect('blog_app:blog', pk=blog.pk)

        return render(request, 'blog_app:add_blog', context=context)
