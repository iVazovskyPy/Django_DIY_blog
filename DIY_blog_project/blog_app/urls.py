from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import IndexView, RegistrationView, MyLoginView, AllBlogsView, BlogView, BloggerView, CommentView, \
    BloggerListView, show_base_template_view, MyProfileView, ProfileEditView, BlogEditView, DeleteBlogView, AddBlogView

app_name = 'blog_app'


urlpatterns = [
    path('base/', show_base_template_view, name='base'),
    path('', IndexView.as_view(), name='index'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='blog_app:index'), name='logout'),
    path('all_blogs/', AllBlogsView.as_view(), name='all_blogs'),
    path('blog/<int:pk>/', BlogView.as_view(), name='blog'),
    path('blog/<int:pk>/<int:blogger_pk>/', BlogView.as_view(), name='blog'),
    path('blogger/<int:pk>/', BloggerView.as_view(), name='blogger'),
    path('comment/<int:pk>/', CommentView.as_view(), name='comment'),
    path('bloggers/', BloggerListView.as_view(), name='bloggers'),
    path('profile/', MyProfileView.as_view(), name='profile'),
    path('edit_profile/', ProfileEditView.as_view(), name='edit_profile'),
    path('edit_blog/<int:pk>/', BlogEditView.as_view(), name='edit_blog'),
    path('deleted/<int:pk>', DeleteBlogView.as_view(), name='deleted'),
    path('add_block/', AddBlogView.as_view(), name='add_blog'),
]
