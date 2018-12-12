from django import forms
from blog.models import Post, Comment, Like, Favorite
from crispy_forms.helper import FormHelper

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'description', 'url',)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment',)

class ContactForm(forms.Form):
    contact_name = forms.CharField(required=True)
    contact_email = forms.EmailField(required=True)
    content = forms.CharField(required=True, widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['contact_name'].label = "Your name:"
        self.fields['contact_email'].label = "Your email:"
        self.fields['content'].label = "What would you like to say?"
