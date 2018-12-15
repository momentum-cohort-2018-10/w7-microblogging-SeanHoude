from rest_framework import serializers
from blog.models import User, Post, Comment, Favorite, Like, Follow

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'is_superuser', 'is_staff', 'is_active', 'users_followed')

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())

    class Meta:
        model = Comment
        fields = ('user', 'comment',)

class PostSerializer(serializers.ModelSerializer):
    liked_by = serializers.SlugRelatedField(slug_field="username", many=True, read_only=True)
    user = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())
    favorited_by = serializers.SlugRelatedField(slug_field="username", many=True, read_only=True)
    post_comments = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='apiv2:comment-detail')

    class Meta:
        model = Post
        fields = ('title', 'user', 'description', 'post_comments', 'slug', 'favorited_by', 'liked_by', 'created',)

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ('user', 'post', 'created', 'updated',)

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('user', 'post', 'created', 'updated',)

class FollowSerializer(serializers.ModelSerializer):
    following = serializers.SlugRelatedField(slug_field="username", read_only=True)
    followed = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())

    class Meta:
        model = Follow
        fields = ('following', 'followed', 'created', 'updated',)
