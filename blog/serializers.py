from rest_framework import serializers
from blog.models import Post, Comment, Favorite, Like, Follow

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        # extra_kwargs = {
        #     'favorited_by': {'write_only': True}
        # }
        fields = ('title', 'user', 'description', 'url', 'slug', 'favorited_by', 'liked_by', 'created', 'updated')

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('user', 'post', 'comment', 'created', 'updated')

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ('user', 'post', 'created', 'updated',)

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('user', 'post', 'created', 'updated',)

class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ('user', 'followed', 'created', 'updated',)
