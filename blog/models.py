from django.contrib.auth.models import User
from django.db import models

from ckeditor.fields import RichTextField
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    @staticmethod
    def get_absolute_url():
        return reverse('home')

    class Meta:
        verbose_name = 'Kategoriya'
        verbose_name_plural = 'Kategoriyalar'


class Post(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = RichTextField()
    snippet = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/post')
    slug = models.CharField(max_length=255)
    likes = models.ManyToManyField(User, related_name='blog_posts', default=None, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title + ' | ' + self.author.username

    @staticmethod
    def get_absolute_url():
        return reverse('home')

    def total_likes(self):
        return self.likes.count()

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Postlar'
        ordering = ['-created_at']


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user', null=True)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    body = models.TextField(verbose_name='Fikringizning to‘liq matni')
    date_add = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[:15] + ' ' + self.user.username

    class Meta:
        ordering = ['-date_add']


class ReplyComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    reply_body = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reply_user')
    date_add = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'reply to ' + str(self.user.username)

    class Meta:
        ordering = ['-date_add']
