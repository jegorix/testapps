from django import forms
from .models import Comment

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,
                               widget=forms.Textarea)

class CommentForm(forms.ModelForm):
    name = forms.CharField(required=True,
                           widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Name"}))
    
    email = forms.EmailField(required=True,
                             widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email"}))
    
    body = forms.CharField(required=True,
                           widget=forms.Textarea(attrs={"class": "form-control", "placeholder": "Text"}))

    class Meta:
        model = Comment
        fields = ["name", "email", "body"]
        

class SearchForm(forms.Form):
    query = forms.CharField()