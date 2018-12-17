from django import forms
from blog.models import Post, Comment, Like, Favorite

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'description', 'url',)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment',)
