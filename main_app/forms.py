from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class TradeSearchForm(forms.Form):
    CHOICES = [('cb_name', ' Find out who owns a Crazy Bone'), ('user_name', 'Find out what Crazy Bones a user has')]
    search_method = forms.ChoiceField(label='Do you want to:', widget=forms.RadioSelect, choices=CHOICES)
    search_query = forms.CharField(label="Enter Name of User or Crazy Bone", max_length=100)

class BattleSearchForm(forms.Form):
    CHOICES = [('cb_name', ' Find out who owns a Crazy Bone'), ('user_name', 'Find out what Crazy Bones a user has')]
    search_method = forms.ChoiceField(label='Do you want to:', widget=forms.RadioSelect, choices=CHOICES)
    search_query = forms.CharField(label="Enter Name of User or Crazy Bone", max_length=100)