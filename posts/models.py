from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
import uuid


class Post(models.Model):
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True)

    # For share functionality we need a field
    # repost = models.ForeignKey(
    #     "self", on_delete=models.CASCADE, related_name='reposts', null=True, blank=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(null=True, blank=True,max_length=255)
    image = models.ImageField(blank=True, null=True)
    comment_count = models.IntegerField(blank=True, null=True, default=0)
    share_count = models.IntegerField(blank=True, null=True, default=0)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    vote_rank = models.IntegerField(blank=True, null=True, default=0)
    votes = models.ManyToManyField(
        User, related_name='post_user', blank=True, through='PostReact')

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.content[0:80]

    # @property
    # def shares(self):
    #     queryset = self.reposts.all()
    #     return queryset

    # @property
    # def comments(self):
    #     # Still need a way to get all sub elemsnts
    #     queryset = self.post_set.all()
    #     return queryset

        # _set to make reverse query


class PostReact(models.Model):
    CHOICES = (
        ('like', 'like'),
        ('dislike', 'dislike')
    )

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, null=True, blank=True)
    value = models.CharField(max_length=20, choices=CHOICES)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return str(self.user) + ' ' + str(self.value) + '"' + str(self.post) + '"'


class Comment(models.Model):


    content = models.TextField(blank=False,null=False,max_length=255)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, null=True, blank=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    created = models.DateTimeField(auto_now_add=True)

    


    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.content
