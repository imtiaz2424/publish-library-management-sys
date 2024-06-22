from django import forms

from .models import Post, Review

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # fields = '__all__'
        exclude = ['users']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review        
        fields = ['name', 'email', 'comment', 'rating']
