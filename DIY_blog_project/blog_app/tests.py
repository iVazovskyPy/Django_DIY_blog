from django.contrib.auth.models import User
from django.test import TestCase
from .models import Blog


class BlogTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username='test_user', first_name='Ivan', last_name='Vazovsky',
                                   password='test_password')
        Blog.objects.create(name='test_blog', content='test_content', blogger=user)

    def test_blog_content(self):
        blog = Blog.objects.get(name='test_blog')
        self.assertEqual(blog.content, 'test_content')
