from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

class Timestamp(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Post(Timestamp):
    title = models.CharField(max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    description = models.TextField()
    url = models.URLField(max_length=400, null=True, blank=True)
    slug = models.SlugField(unique=True, max_length=50)
    favorited_by = models.ManyToManyField(User, through='Favorite', related_name='favorite_posts')
    liked_by = models.ManyToManyField(User, through='Like', related_name='liked_posts')

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return "posts/%s/" % self.slug

class Comment(Timestamp):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, related_name="comments")
    comment = models.CharField(max_length=400)

    def __str__(self):
        return self.comment

class Favorite(Timestamp):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="favoriters")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, related_name="favorites")

    class Meta:
        unique_together = ('post', 'user',)

class Like(Timestamp):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="likers")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, related_name="likes")

    class Meta:
        unique_together = ('post', 'user',)

class Follow(Timestamp):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="followers")
    followed = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, related_name="followed")
