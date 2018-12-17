from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import AbstractUser

class Timestamp(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class User(AbstractUser):
    # users_followed returns all users a specific user (clinton) is following.
    #   ex clinton following Rondale and Peter
    #   clinton = User.objects.create('clinton')
    #   clinton.users_followed.all() - // <queryset[<user: rondale>, <user: peter>]>

    # followers returns all users a specific user (tiana) is followed by.
    #   ex. Clinton and Rondale following Tiana
    #   tiana = User.objects.create('clinton')
    #   tiana.followers.all() - // <queryset[<user: clinton>, <user: rondale>]>
    users_followed = models.ManyToManyField(to='User', through='Follow', through_fields=('following', 'followed'), related_name="followers")

class Follow(Timestamp):
    following = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="is_following")
    followed = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="followed_by")

    class Meta:
        unique_together = ('following', 'followed',)

    def __str__(self):
        return f"Following: {self.following}, Followed: {self.followed}"

class Post(Timestamp):
    title = models.CharField(max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    description = models.TextField()
    url = models.URLField(max_length=400, null=True, blank=True)
    slug = models.SlugField(unique=True, max_length=250)
    favorited_by = models.ManyToManyField(User, through='Favorite', related_name='favorite_posts')
    liked_by = models.ManyToManyField(User, through='Like', related_name='liked_posts')
    commented_by = models.ManyToManyField(User, through='comment', related_name='commented_posts')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return "posts/%s/" % self.slug

class Comment(Timestamp):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="user_comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, related_name="post_comments")
    comment = models.CharField(max_length=400)

    def __str__(self):
        return self.comment

class Favorite(Timestamp):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="favoriters")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, related_name="favorites")

    class Meta:
        unique_together = ('post', 'user',)

    def __str__(self):
        return f"User: {self.user}, Post: {self.post}"

class Like(Timestamp):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="likers")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, related_name="likes")

    class Meta:
        unique_together = ('post', 'user',)

    def __str__(self):
        return f"User: {self.user}, Post: {self.post}"
