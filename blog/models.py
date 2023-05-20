from django.db import models
from django.utils.text import Truncator
from django.urls import reverse
from django.contrib.auth.models import User


class Blog(models.Model):
    """Model representing blog posts."""
    title = models.CharField(max_length=200, help_text='Enter title')
    blogger = models.ForeignKey('Blogger', on_delete=models.SET_NULL, null=True)
    post = models.TextField(max_length=1000, help_text='Enter post')
    post_date = models.DateField(auto_now_add=True)

    def __str__(self):
        """String representation of model"""
        return self.title

    def get_absolute_url(self):
        """Returns the URL to access a detail record for this blog."""
        return reverse('blog_detail', kwargs={'pk': self.pk})


class Blogger(models.Model):
    """Model representing blogger"""
    name = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    bio = models.TextField(max_length=1000, help_text='Enter bio')

    def __str__(self):
        """String representation of model"""
        return str(self.name)

    def get_absolute_url(self):
        """Returns the URL to access a detail record for this blogger."""
        return reverse('blogger_detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    """Model representing comments"""
    description = models.TextField(max_length=1000)
    comment_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    comment_date = models.DateField(auto_now_add=True)
    comment_on = models.ForeignKey('Blog', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        truncated_comment = Truncator(self.description)
        return truncated_comment.chars(75)


