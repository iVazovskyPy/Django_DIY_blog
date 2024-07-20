from django.contrib.auth.models import User
from django.test import TestCase
from .models import Blog, Profile
from django.urls import reverse


class BlogTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username='test_user', first_name='Ivan', last_name='Vazovsky',
                                   password='test_password')
        Blog.objects.create(name='test_blog', content='test_content', blogger=user)

    def test_blog_content(self):
        blog = Blog.objects.get(name='test_blog')
        self.assertEqual(blog.content, 'test_content')


class GetBloggerTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username='test_user', first_name='Ivan', last_name='Vazovsky',
                                   password='test_password')
        Profile.objects.create(user=user, bio='test_bio', phone_number=1)

    def test_get_blogger(self):
        response = self.client.get(reverse('blog_app:blogger', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ivan')


class TemplateTestCase(TestCase):
    def test_is_template_used(self):
        response = self.client.get(reverse('blog_app:registration'))
        self.assertTemplateUsed(response, 'blog_app/register.html')


class PaginationTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username='test_user', first_name='Ivan', last_name='Vazovsky',
                                   password='test_password')
        for i_num in range(6):
            Blog.objects.create(name=f'test_blog{i_num}', content=f'test_content{i_num}', blogger=user)

    def test_blogs_pagination(self):
        response = self.client.get(reverse('blog_app:all_blogs'))
        self.assertEqual(len(response.context['page_obj']), 5)
