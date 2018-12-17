from rest_framework import serializers
from rest_framework.reverse import reverse
from blog.models import User, Post, Comment, Favorite, Like, Follow

# more streamlined serializers
class FollowedSerializer(serializers.ModelSerializer):
    following = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())

    class Meta:
        model = Follow
        fields = ('following',)

class FollowingSerializer(serializers.ModelSerializer):
    followed = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())

    class Meta:
        model = Follow
        fields = ('followed',)

class UserSerializer(serializers.ModelSerializer):
    user_url = serializers.HyperlinkedIdentityField(view_name="apiv2:user-detail")
    is_following = FollowingSerializer(many=True, read_only=True)
    followed_by = FollowedSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('username', 'user_url', 'email', 'is_superuser', 'is_staff', 'is_active', 'followed_by', 'is_following')

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())
    comment_url = serializers.HyperlinkedIdentityField(view_name='apiv2:comment-detail', )

    class Meta:
        model = Comment
        fields = ('user', 'comment', 'comment_url')

class PostSerializer(serializers.ModelSerializer):
    title_url = serializers.HyperlinkedIdentityField(view_name="apiv2:post-detail")
    liked_by = serializers.SlugRelatedField(slug_field="username", many=True, read_only=True)
    user = UserSerializer(read_only=True)
    favorited_by = serializers.SlugRelatedField(slug_field="username", many=True, read_only=True)
    post_comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('title', 'title_url', 'user', 'description', 'post_comments', 'favorited_by', 'liked_by', 'created',)

# deprecated serializer from api v1
class FollowSerializer(serializers.ModelSerializer):
    following = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())
    followed = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())

    class Meta:
        model = Follow
        fields = ('following', 'followed')
