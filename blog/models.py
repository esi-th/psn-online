from django.db import models
from django.contrib.auth import get_user_model
from django.shortcuts import reverse


class Category(models.Model):
    name = models.CharField('Category Name', max_length=255)
    description = models.CharField('Description', max_length=255, blank=True)
    datetime_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField('Name', max_length=50)

    def __str__(self):
        return self.name


class Post(models.Model):
    POST_STATUS_PUBLISHED = 'p'
    POST_STATUS_DRAFT = 'd'
    POST_STATUS_CHOICES = [
        (POST_STATUS_PUBLISHED, 'Published'),
        (POST_STATUS_DRAFT, 'Draft'),
    ]
    title = models.CharField('Title', max_length=255)
    content = models.TextField('Content')
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='Author')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Category')
    status = models.CharField('Status', max_length=2, choices=POST_STATUS_CHOICES, default=POST_STATUS_DRAFT)
    slug = models.SlugField(unique=True, blank=True)
    tags = models.ManyToManyField(Tag, verbose_name='Tags')
    likes = models.ManyToManyField(get_user_model(), related_name='blog_post', blank=True)
    datetime_modified = models.DateTimeField('Modified On', auto_now=True)
    datetime_created = models.DateTimeField('Created On', auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.id])


class Comment(models.Model):
    COMMENT_STATUS_WAITING = 'w'
    COMMENT_STATUS_APPROVED = 'a'
    COMMENT_STATUS_NOT_APPROVED = 'na'
    COMMENT_STATUS_CHOICES = [
        (COMMENT_STATUS_WAITING, 'Waiting'),
        (COMMENT_STATUS_APPROVED, 'Approved'),
        (COMMENT_STATUS_NOT_APPROVED, 'Not Approved'),
    ]
    body = models.CharField('Comment Text', max_length=1000)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                               verbose_name='Author', related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Post', related_name='comments')
    status = models.CharField(max_length=2, choices=COMMENT_STATUS_CHOICES, default=COMMENT_STATUS_WAITING)
    reply_to = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    datetime_modified = models.DateTimeField('Modified On', auto_now=True)
    datetime_created = models.DateTimeField('Created On', auto_now_add=True)

    def __str__(self):
        return f'ID: {self.id} | Post: {self.post} | Author: {self.author}'

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.post.id])
