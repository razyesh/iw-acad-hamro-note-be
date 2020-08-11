from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Blog,Category

class BlogTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # create a user
        testuser1 = get_user_model().objects.create_user(
            username = 'testuser1',
            email = 'test@gmail.com',
            password = '123456789'
        )
        testuser1.save()
        # create a blog
        programming = Category.objects.create(name='Python')
        test_post = Blog.objects.create(
            user = testuser1,
            title = 'New Blog title',
            subtitle = 'simple title',
            category = programming,
            meta_description = ' a web app blog testing haha',
            content = 'Content will goes here.',
        )
        test_post.save()

    def test_blog_content(self):
        post = Blog.objects.get(id=1)
        user = f'{post.user}'
        title = f'{post.title}'
        category = f'{post.category}'
        subtitle = f'{post.subtitle}'
        meta_description = f'{post.meta_description}'
        content = f'{post.content}'
        
        self.assertEqual(user,'testuser1','testuser1')
        self.assertEqual(title,'New Blog title')
        self.assertEqual(subtitle,'simple title')
        self.assertEqual(meta_description,' a web app blog testing haha')
        self.assertEqual(content,'Content will goes here.')
