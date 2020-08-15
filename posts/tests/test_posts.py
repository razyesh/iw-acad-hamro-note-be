import os
from django.conf import settings
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from ..models import Post

USER = get_user_model()


def create_post():
    post = Post()
    post.post_slug = 'test-post'
    post.caption = ('This is a new post. This is just for the test '
                    'purpose.')
    print('Creating file...')
    f = open('test_file.txt', 'w', newline='', )
    f.write('Hello this is the test_file.')
    f.close()
    print('File created...')
    post.file = 'test_file.txt'
    return post


class TestPostCase(APITestCase):

    def create_user(self):
        """
        Creates the test User once.
        """
        u = USER.objects.create(username='test_user1',
                                email='test_email@example.com', )
        u.set_password('test_password')
        u.save()
        self.user = u
        return u

    def setUp(self):
        """This creates a post instance in database"""
        self.post = create_post()
        self.post.user = self.create_user()
        self.post.save()

    def tearDown(self):
        print('Deleting user')
        self.user.delete()
        print('Deleted user')
        print('*' * 30)
        print('Deleting post.')
        self.post.delete()
        print('Deleted post and user.')
        print('*' * 30)
        print('Deleting test_file...')
        if os.path.exists(settings.BASE_DIR / 'test_file.txt'):
            os.remove(settings.BASE_DIR / 'test_file.txt')
            print('Deleted file')
        print()
        print()

    def test_if_str_representation_works_fine(self):
        """To ensure our post str representation works fine."""
        self.assertEqual(str(self.post), f'{self.post.caption[:20]}...')

    def test_if_post_list_is_returned_as_response(self):
        """
        To test if list is returned successfully.
        """
        response = self.client.get(reverse('posts:posts_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        explore_response = self.client.get(reverse('posts:posts_explore'))
        self.assertEqual(explore_response.status_code, status.HTTP_200_OK)

    def get_create_response(self):
        f = open('test_file.txt', 'w+', newline='', )
        f.write('Hello this is the test_file for response.')
        f.close()

        data = {
            'user': self.user.id,
            'caption': 'This is a post created from test',
            'file': ''
        }
        return self.client.post(reverse('posts:post_create'), data=data,
                                format='multipart')

    def test_if_we_can_create_post_via_api(self):
        """
        This asserts if we can create a post via api endpoint.
        """
        create_response = self.get_create_response()
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)

    def test_if_we_can_update_via_api(self):
        """
        This asserts if we can update a post via api endpoint.
        """
        create_response = self.get_create_response()
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        post = Post.objects.get(id=1)
        update_response = self.client.put(reverse('posts:post_update',
                                                  kwargs={
                                                      'post_slug':
                                                          post.post_slug
                                                  }),
                                          data={
                                              'user': self.user.id,
                                              'post_slug': post.post_slug,
                                              'caption':
                                                  'This is a post '
                                                  'updated from test',
                                              'file': ''
                                          }, format='multipart')
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        update_response = self.client.patch(reverse('posts:post_update',
                                                    kwargs={
                                                        'post_slug':
                                                            post.post_slug
                                                    }),
                                            data={
                                                'caption':
                                                    'This is a post '
                                                    'updated from test with '
                                                    'patch',
                                            }, format='multipart')
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)

    def test_if_retrieve_update_view_works_fine(self):
        create_response = self.get_create_response()
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        post_slug = create_response.data['post_slug']
        get_response = self.client.get(reverse('posts:post_get_delete',
                                               kwargs={
                                                   'post_slug': post_slug
                                               }))
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        delete_response = self.client.delete(reverse('posts:post_get_delete',
                                                     kwargs={
                                                         'post_slug': post_slug
                                                     }))
        self.assertEqual(delete_response.status_code,
                         status.HTTP_204_NO_CONTENT)

    def like_unlike_post(self, post_slug='', action='like'):
        return self.client.post(reverse('posts:like_unlike_post', kwargs={
            'post_slug': post_slug,
            'action': action
        }))

    def test_if_like_unlike_view_works_fine(self):
        create_response = self.get_create_response()
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        post_slug = create_response.data['post_slug']
        like_response = self.like_unlike_post(post_slug=post_slug)
        self.assertEqual(like_response.status_code, status.HTTP_200_OK)
        self.assertEqual(like_response.data['stars_count'], 1)
        like_response = self.like_unlike_post(post_slug=post_slug)
        self.assertEqual(like_response.status_code, status.HTTP_200_OK)
        self.assertEqual(like_response.data['stars_count'], 2)
        unlike_response = self.like_unlike_post(
                post_slug=post_slug,
                action='unlike'
        )
        self.assertEqual(unlike_response.status_code, status.HTTP_200_OK)
        self.assertEqual(unlike_response.data['stars_count'], 1)
        unlike_response = self.like_unlike_post(
                post_slug=post_slug,
                action='unlike'
        )
        self.assertEqual(unlike_response.status_code, status.HTTP_200_OK)
        self.assertEqual(unlike_response.data['stars_count'], 0)
        # to ensure the likes count does not get below zero i.e. negative
        unlike_response = self.like_unlike_post(
                post_slug=post_slug,
                action='unlike'
        )
        self.assertEqual(unlike_response.status_code, status.HTTP_200_OK)
        self.assertEqual(unlike_response.data['stars_count'], 0)
