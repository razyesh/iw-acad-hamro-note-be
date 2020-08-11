from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Blog

User = get_user_model()

class BlogTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # create a user
        testuser = User.objects.create_user(
            username = 'testuser1',
            password = '123456789'
        )
        testuser.save()
        # create a blog
        test_post = Blog.objects.create(
            user = testuser,
            title = 'New Blog title',
            subtitle = 'simple title',
            meta_description = ' a web app blog testing haha',
            content = 'Content will goes here.',
        )
        test_post.save()

    def test_blog_content(self):
        post = Blog.objects.get(id=1)
        user = f'{post.user}'
        title = f'{post.title}'
        subtitle = f'{post.subtitle}'
        meta_description = f'{post.meta_description}'
        content = f'{post.content}'
        
        self.assertEqual(user,'testuser')
        self.assertEqual(title,'New Blog title')
        self.assertEqual(subtitle,'simple title')
        self.assertEqual(meta_description,' a web app blog testing haha')
        self.assertEqual(content,'Content will goes here.')
