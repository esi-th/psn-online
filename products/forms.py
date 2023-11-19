from django import forms
from .models import Comment, Review


class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']


class NewReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['body', 'stars', 'recommend', ]
