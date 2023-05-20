from django.contrib.auth.models import User
from django.urls import resolve, reverse
from django.test import TestCase
from ..models import Blog, Blogger, Comment
from ..views import BlogDetailView, BloggerDetailView, BlogListView, BloggerListView, index


class IndexTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='testuser', password='password123')

    def test_index_view_status_code(self):
        url = reverse('index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_index_view_uses_correct_template(self):
        url = reverse('index')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'blog/index.html')

    def test_index_url_resolve_index_view(self):
        view = resolve('/blog/')
        self.assertEqual(view.func, index)

    def test_index_view_has_link_to_home_page(self):
        home_url = reverse('index')
        response = self.client.get(home_url)
        self.assertContains(response, f'href="{home_url}"')

    def test_index_view_has_link_to_all_blogs_page(self):
        url = reverse('index')
        all_blog_url = reverse('blogs')
        response = self.client.get(url)
        self.assertContains(response, f'href="{all_blog_url}"')

    def test_index_view_has_link_to_all_bloggers_page(self):
        url = reverse('index')
        all_blogger_url = reverse('bloggers')
        response = self.client.get(url)
        self.assertContains(response, f'href="{all_blogger_url}"')

    def test_index_view_has_link_to_login_page(self):
        url = reverse('index')
        login_url = reverse('login')
        response = self.client.get(url)
        self.assertContains(response, f'href="{login_url}?next="')

    def test_index_view_has_link_to_logout_if_logged_in(self):
        login = self.client.login(username='testuser', password='password123')
        url = reverse('login')
        response = self.client.get(url)
        self.assertEqual(str(response.context['user']), 'testuser')
        self.assertEqual(response.status_code, 200)
        logout_url = reverse('logout')
        response = self.client.get(reverse('index'))
        self.assertContains(response, f'href="{logout_url}?next=/blog/"')

    def test_index_view_displays_user_name_if_logged_in(self):
        login = self.client.login(username='testuser', password='password123')
        url = reverse('login')
        response = self.client.get(url)
        self.assertEqual(str(response.context['user']), 'testuser')
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('index'))
        self.assertContains(response, 'User: testuser')


class BlogListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_blogs = 15
        for blog_id in range(number_of_blogs):
            user = User.objects.create_user(username=f'testuser{blog_id}', password=f'password{blog_id}')
            blogger = Blogger.objects.create(name=user)
            Blog.objects.create(title='Test Post', post='This is a post', blogger=blogger)

    def test_pagination_is_5(self):
        response = self.client.get(reverse('blogs'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['blog_list']), 5)

    def test_lists_all_blogs(self):
        response = self.client.get(reverse('blogs') + '?page=1')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['blog_list']), 5)

    def test_view_url_exists_at_desired_location(self):
        view = resolve('/blog/blogs/')
        self.assertEqual(view.func.view_class, BlogListView)

    def test_view_url_has_correct_response_code(self):
        response = self.client.get('/blog/blogs/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('blogs'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('blogs'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blog_list.html')

    def test_page_ordered_by_newest_post_first(self):
        response = self.client.get(reverse('blogs'))
        last_date = 0
        for blog in response.context['blog_list']:
            if last_date == 0:
                last_date = blog.post_date
            else:
                self.assertTrue(last_date >= blog.post_date)
                last_date = blog.post_date


class BloggerListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_bloggers = 15
        for blogger_id in range(number_of_bloggers):
            user = User.objects.create_user(username=f'testuser{blogger_id}', password=f'password{blogger_id}')
            Blogger.objects.create(name=user)

    def test_lists_all_bloggers(self):
        response = self.client.get(reverse('bloggers'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['blogger_list']), 15)

    def test_view_url_exists_at_desired_location(self):
        view = resolve('/blog/bloggers/')
        self.assertEqual(view.func.view_class, BloggerListView)

    def test_view_url_has_correct_response_code(self):
        response = self.client.get('/blog/bloggers/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('bloggers'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('bloggers'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blogger_list.html')


class CommentCreateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(username='testuser', password='password123')
        blogger = Blogger.objects.create(name=test_user, bio='bio')
        Blog.objects.create(title='test', blogger=blogger, post='post')

    def test_if_logged_in_to_create_comment(self):
        login = self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('create', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)

    def test_redirect_if_not_logged_in(self):
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        response = self.client.get(reverse('create', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_view_uses_correct_template(self):
        login = self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('create', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/comment_form.html')

    def test_view_redirects_to_blog_detail_view_on_success(self):
        login = self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('create', kwargs={'pk': 1}), {'description': 'this is a comment'})
        self.assertRedirects(response, reverse('blog_detail', kwargs={'pk': 1}))

    def test_view_posts_to_blog_detail_view_successfully(self):
        login = self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('create', kwargs={'pk': 1}), {'description': 'this is a comment'})
        response = self.client.get(reverse('blog_detail', kwargs={'pk': 1}))
        self.assertContains(response, 'this is a comment')


class BlogDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(username='testuser', password='password123')

        blogger = Blogger.objects.create(name=test_user, bio='bio')

        blog = Blog.objects.create(title='test', blogger=blogger, post='post')

        for comment in range(16):
            Comment.objects.create(description='hello', comment_by=test_user, comment_on=blog)

    def test_view_url_exists_at_desired_location(self):
        view = resolve('/blog/blogs/1/')
        self.assertEqual(view.func.view_class, BlogDetailView)

    def test_view_url_has_correct_response_code(self):
        response = self.client.get('/blog/blogs/1/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('blog_detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('blog_detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blog_detail.html')

    def test_index_view_has_link_to_blogger_detail_page(self):
        url = reverse('blogger_detail', kwargs={'pk': 1})
        response = self.client.get(reverse('blog_detail', kwargs={'pk': 1}))
        self.assertContains(response, f'href="{url}"')


class BloggerDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(username='testuser', password='password123')
        blogger = Blogger.objects.create(name=test_user, bio='bio')
        Blog.objects.create(title='test', blogger=blogger, post='post')

    def test_view_url_exists_at_desired_location(self):
        view = resolve('/blog/bloggers/1/')
        self.assertEqual(view.func.view_class, BloggerDetailView)

    def test_view_url_has_correct_response_code(self):
        response = self.client.get('/blog/bloggers/1/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('blogger_detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('blogger_detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blogger_detail.html')

    def test_index_view_has_link_to_blogger_detail_page(self):
        url = reverse('blog_detail', kwargs={'pk': 1})
        response = self.client.get(reverse('blogger_detail', kwargs={'pk': 1}))
        self.assertContains(response, f'href="{url}"')