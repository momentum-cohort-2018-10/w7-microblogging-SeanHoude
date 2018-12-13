from django.contrib import admin
from blog.models import User, Post, Comment, Favorite, Like, Follow

class PostAdmin(admin.ModelAdmin):
    model = Post
    list_display = ('title', 'user', 'description', 'url', 'slug', 'created', 'updated')
    prepopulated_fields = {'slug': ('title',)}

class CommentAdmin(admin.ModelAdmin):
    model = Comment
    list_display = ('user', 'post', 'comment', 'created', 'updated', )

class FavoriteAdmin(admin.ModelAdmin):
    model = Favorite
    list_display = ('user', 'post', 'created', 'updated', )

class LikeAdmin(admin.ModelAdmin):
    model = Like
    list_display = ('user', 'post', 'created', 'updated', )

class FollowersInline(admin.StackedInline):
    model = Follow
    verbose_name = 'followed_by'
    fk_name = 'followed'
    fields = ('following',)
    extra = 1

class FollowingInline(admin.StackedInline):
    verbose_name = 'is_following'
    model = Follow
    fk_name = 'following'
    fields = ('followed',)
    extra = 1

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    model = Follow
    list_display = ('following', 'followed',)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = ('username', 'email', 'is_superuser', 'is_staff', 'is_active',)
    inlines = [FollowersInline, FollowingInline]

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Like, LikeAdmin)
