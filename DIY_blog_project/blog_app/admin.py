from django.contrib import admin

from .models import Blog, Comment, Profile


@admin.register(Blog)
class AdminBlog(admin.ModelAdmin):
    list_display = ['name', 'content', 'blogger', 'publication_date']


@admin.register(Comment)
class AdminComment(admin.ModelAdmin):
    list_display = ['user', 'blog', 'publication_date', 'description']


@admin.register(Profile)
class AdminProfile(admin.ModelAdmin):
    list_display = ['user', 'bio', 'phone_number', 'profile_photo']

