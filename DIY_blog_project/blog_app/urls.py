from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import IndexView, RegistrationView, MyLoginView, AllBlogsView, BlogView, BloggerView, CommentView, \
    BloggerListView

app_name = 'blog_app'


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='blog_app:login'), name='logout'),
    path('all_blogs/', AllBlogsView.as_view(), name='all_blogs'),
    path('blog/<int:pk>/', BlogView.as_view(), name='blog'),
    path('blog/<int:pk>/<int:blogger_pk>/', BlogView.as_view(), name='blog'),
    path('blogger/<int:pk>/', BloggerView.as_view(), name='blogger'),
    path('comment/<int:pk>', CommentView.as_view(), name='comment'),
    path('bloggers/', BloggerListView.as_view(), name='bloggers'),
]
