from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class TradeSearchForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)