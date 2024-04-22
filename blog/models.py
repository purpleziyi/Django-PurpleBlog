from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class BlogCategory(models.Model):
    name = models.CharField(max_length=200, verbose_name='categoty name')

    def __str__(self):
        return self.name

    class Meta:
        # apple, apples
        verbose_name = 'Blog Category'
        verbose_name_plural = 'Blog Categories'


class Blog(models.Model):
    title = models.CharField(max_length=200, verbose_name='title')
    content = models.TextField(verbose_name='content')
    pub_time = models.DateTimeField(auto_now_add=True, verbose_name='publishtime')
    category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE, verbose_name='category')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='author')

    def __str__(self):
        return self.title

    class Meta:
        # apple, apples
        verbose_name = 'blog'
        verbose_name_plural = 'blogs'
        ordering = ['-pub_time']


class BlogComment(models.Model):
    content = models.TextField(verbose_name='content')
    pub_time = models.DateTimeField(auto_now_add=True, verbose_name='publish time')
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments', verbose_name='Blog')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='author')

    def __str__(self):
        return self.content

    class Meta:
        # apple, apples
        verbose_name = 'Blog Comment'
        verbose_name_plural = 'Blog Comments'
        ordering = ['-pub_time']

