import os
from django.urls import reverse
from rest_framework.test import APITestCase

from ..models import Comment
from .test_posts import create_post, USER
from rest_framework import status


class TestCommentCase(APITestCase):

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
        """Initial setup. Actions to be performed before each test."""
        self.comment = Comment()
        self.comment.comment_description = 'This is a test comment'
        self.post = create_post()
        self.post.user = self.create_user()
        self.post.save()
        self.comment.post = self.post
        self.comment.user = self.user
        self.comment.save()

    def tearDown(self):
        """Actions to be performed after each test."""
        self.comment.post.delete()
        self.user.delete()

        print('Deleting comment...')
        self.comment.delete()
        print('Deleted comment.')
        print('Deleting test_file...')
        if os.path.exists('test_file.txt'):
            os.remove('test_file.txt')
            print('Deleted file')
        print()
        print()

    def test_str_representation(self):
        """
        To test our string representation of the model.
        """
        self.assertEqual(str(self.comment),
                         f'{self.comment.comment_description[:20]}...')

    def test_comment_list_get(self):
        """
        To ensure our listing api is working perfectly.
        """
        response = self.client.get(reverse('posts:comment_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_comment_creation(self):
        """
        To test if we can create the comment via our api endpoint.
        """
        response = self.client.post(reverse('posts:comment_create'),
                                    data={
                                        'post': self.post.id,
                                        'user': self.user.id,
                                        'comment_description': 'This is a '
                                                               'test_comment'
                                    }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {
            'post': self.post.id,
            'user': self.user.id,
            'comment_description': 'This is a '
                                   'test_comment'
        })

    def test_comment_get_deletion(self):
        """
        To test if the comment gets deleted with the api.
        """
        create_response = self.client.post(reverse('posts:comment_create'),
                                           data={
                                               'post': self.post.id,
                                               'user': self.user.id,
                                               'comment_description':
                                                   'This is a test_comment'
                                           }, format='json')
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        get_response = self.client.get(reverse('posts:comment_get_delete',
                                               kwargs={'pk': '1'}))
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)

        delete_response = self.client.delete(
                reverse('posts:comment_get_delete', kwargs={'pk': '1'})
        )
        self.assertEqual(delete_response.status_code,
                         status.HTTP_204_NO_CONTENT)

    def test_comment_update(self):
        """
        To assert the api endpoint is working as expected with put and patch
        method.
        """
        create_response = self.client.post(reverse('posts:comment_create'),
                                           data={
                                               'post': self.post.id,
                                               'user': self.user.id,
                                               'comment_description':
                                                   'This is a test_comment'
                                           }, format='json')
        # assert that the comment is created. via json
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        # the comment should be updated with a put response.
        update_response = self.client.put(reverse('posts:comment_update',
                                                  kwargs={'pk': '1'}),
                                          data={
                                              'post': self.post.id,
                                              'user': self.user.id,
                                              'comment_description':
                                                  'This is a test_comment '
                                                  'updated'
                                          }, format='json')
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        # assert the updated data in the response
        self.assertEqual(update_response.data, {
            'post': self.post.id,
            'user': self.user.id,
            'comment_description':
                'This is a test_comment '
                'updated'
        }, msg='The put request update test Passed!!')
        # the endpoint should also work with th http patch method as well.
        update_patch_response = self.client.patch(
                reverse('posts:comment_update', kwargs={'pk': '1'}),
                data={'comment_description': 'This is a test comment updated0'},
                format='json'
        )
        self.assertEqual(update_patch_response.status_code,
                         status.HTTP_200_OK)
        self.assertEqual(update_patch_response.data, {
            'post': self.post.id,
            'user': self.user.id,
            'comment_description':
                'This is a test comment updated0'
        }, msg='patch method update test passed')

    def like_unlike_comment(self, pk='1', action='like'):
        """Function for liking and unliking a comment.
        returns a response"""
        return self.client.post(reverse('posts:like_unlike_comment',
                                        kwargs={
                                            'pk': pk,
                                            'action': action
                                        }))

    def test_like_unlike_works_without_error(self):
        """
        Test whether the like/unlike api endpoint works as expected.
        """
        create_response = self.client.post(reverse('posts:comment_create'),
                                           data={
                                               'post': self.post.id,
                                               'user': self.user.id,
                                               'comment_description':
                                                   'This is a test_comment'
                                           }, format='json')
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        # initial stars_count is zero, so when liked must increase by 1
        like_response = self.like_unlike_comment()
        self.assertEqual(like_response.status_code, status.HTTP_200_OK)
        self.assertEqual(like_response.data['stars_count'], 1)
        like_again = self.like_unlike_comment()
        self.assertEqual(like_again.status_code, status.HTTP_200_OK)
        self.assertEqual(like_again.data['stars_count'], 2)
        # current likes/stars count is 2 so if unliked should become 1
        unlike_comment_response = self.like_unlike_comment(pk='1',
                                                           action='unlike')
        self.assertEqual(unlike_comment_response.status_code,
                         status.HTTP_200_OK)
        self.assertEqual(unlike_comment_response.data['stars_count'], 1)
        # current likes/stars count is 1 so if unliked should become 0
        unlike_comment_response = self.like_unlike_comment(pk='1',
                                                           action='unlike')
        self.assertEqual(unlike_comment_response.status_code,
                         status.HTTP_200_OK)
        self.assertEqual(unlike_comment_response.data['stars_count'], 0)
        # current likes/stars count is 0 so if unliked should remain 0
        unlike_comment_response = self.like_unlike_comment(pk='1',
                                                           action='unlike')
        self.assertEqual(unlike_comment_response.status_code,
                         status.HTTP_200_OK)
        self.assertEqual(unlike_comment_response.data['stars_count'], 0)
