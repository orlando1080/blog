from ..models import Blog, Blogger, Comment
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils.text import Truncator


class BlogModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='testuser', password='password123')
        blogger = Blogger.objects.create(name=user)
        Blog.objects.create(title='Test Post', post='This is a post', blogger=blogger)

    def test_title_label(self):
        blog = Blog.objects.get(id=1)
        field_label = blog._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_title_max_length(self):
        blog = Blog.objects.get(id=1)
        max_length = blog._meta.get_field('title').max_length
        self.assertEqual(max_length, 200)

    def test_blogger_name(self):
        blog = Blog.objects.get(id=1)
        expected_blogger_name = str(blog.blogger.name)
        self.assertEqual(expected_blogger_name, 'testuser')

    def test_post_label(self):
        blog = Blog.objects.get(id=1)
        field_label = blog._meta.get_field('post').verbose_name
        self.assertEqual(field_label, 'post')

    def test_post_max_length(self):
        blog = Blog.objects.get(id=1)
        max_length = blog._meta.get_field('post').max_length
        self.assertEqual(max_length, 1000)

    def test_str_representation(self):
        blog = Blog.objects.get(id=1)
        expected_object_name = f'{blog.title}'
        self.assertEqual(str(blog), expected_object_name)

    def test_get_absolute_url(self):
        blog = Blog.objects.get(id=1)
        self.assertEqual(blog.get_absolute_url(), '/blog/blogs/1/')


class BloggerModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='testuser', password='password123')
        Blogger.objects.create(name=user)

    def test_blogger_name(self):
        blogger = Blogger.objects.get(id=1)
        expected_blogger_name = str(blogger.name)
        self.assertEqual(expected_blogger_name, 'testuser')

    def test_bio_max_length(self):
        blogger = Blogger.objects.get(id=1)
        max_length = blogger._meta.get_field('bio').max_length
        self.assertEqual(max_length, 1000)

    def test_bio_label(self):
        blogger = Blogger.objects.get(id=1)
        field_label = blogger._meta.get_field('bio').verbose_name
        self.assertEqual(field_label, 'bio')

    def test_str_representation(self):
        blogger = Blogger.objects.get(id=1)
        expected_object_name = f'{str(blogger.name)}'
        self.assertEqual(str(blogger), expected_object_name)

    def test_get_absolute_url(self):
        blogger = Blogger.objects.get(id=1)
        self.assertEqual(blogger.get_absolute_url(), '/blog/bloggers/1/')


class CommentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create_user(username='testuser1', password='password123')
        user2 = User.objects.create_user(username='testuser2', password='password456')
        blogger1 = Blogger.objects.create(name=user1)
        # blogger2 = Blogger.objects.create(name=user2)
        blog = Blog.objects.create(title='Test Post', post='This is a post', blogger=blogger1)
        description = '''This is a comment that has more than 75 character so I can see if truncated is actually
         working as expected.'''
        Comment.objects.create(description=description, comment_on=blog, comment_by=user2)

    def test_comment_description_max_length(self):
        comment = Comment.objects.get(id=1)
        max_length = comment._meta.get_field('description').max_length
        self.assertEqual(max_length, 1000)

    def test_comment_description_label(self):
        comment = Comment.objects.get(id=1)
        field_label = comment._meta.get_field('description').verbose_name
        self.assertEqual(field_label, 'description')

    def test_comment_by_name(self):
        comment = Comment.objects.get(id=1)
        expected_comment_by_name = str(comment.comment_by)
        self.assertEqual(expected_comment_by_name, 'testuser2')

    def test_comment_on_name(self):
        comment = Comment.objects.get(id=1)
        expected_comment_on_name = str(comment.comment_on)
        self.assertEqual(expected_comment_on_name, 'Test Post')

    def test_str_representation_truncated_comment(self):
        comment = Comment.objects.get(id=1)
        expected_object_length = len(str(comment))
        self.assertEqual(75, expected_object_length)


