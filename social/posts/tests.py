from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Post

class PostTests(APITestCase):

    def setUp(self):
        # Create two users for testing
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password123')

        # Create tokens for both users
        self.token1 = Token.objects.create(user=self.user1)
        self.token2 = Token.objects.create(user=self.user2)

        # Create a post by user1
        self.post1 = Post.objects.create(owner=self.user1, content="This is user1's post.")

    def test_list_posts(self):
        """
        Ensure we can retrieve all posts (available to everyone).
        """
        url = reverse('post-list')  # DRF automatically uses 'post-list' for PostViewSet's list view
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_post_authenticated(self):
        """
        Ensure authenticated users can create posts.
        """
        # Set up token-based authentication
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1.key)
        url = reverse('post-list')
        data = {'content': 'A new post by user1'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)
        self.assertEqual(Post.objects.last().content, 'A new post by user1')

    def test_create_post_unauthenticated(self):
        """
        Ensure unauthenticated users cannot create posts.
        """
        url = reverse('post-list')
        data = {'content': 'Unauthorized post'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Post.objects.count(), 1)  # Still only one post

    def test_update_post_owner(self):
        """
        Ensure a post owner can update their post.
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1.key)
        url = reverse('post-detail', args=[self.post1.id])
        data = {'content': 'Updated post content'}
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post1.refresh_from_db()
        self.assertEqual(self.post1.content, 'Updated post content')

    def test_update_post_not_owner(self):
        """
        Ensure non-owners cannot update someone else's post.
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token2.key)  # Set up token-based authentication
        url = reverse('post-detail', args=[self.post1.id])
        data = {'content': 'User2 trying to update user1 post'}
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.post1.refresh_from_db()
        self.assertNotEqual(self.post1.content, 'User2 trying to update user1 post')

    def test_delete_post_owner(self):
        """
        Ensure the post owner can delete their post.
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1.key)
        url = reverse('post-detail', args=[self.post1.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 0)  # No posts should remain

    def test_delete_post_not_owner(self):
        """
        Ensure non-owners cannot delete someone else's post.
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token2.key)
        url = reverse('post-detail', args=[self.post1.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Post.objects.count(), 1)  # Post should still exist
