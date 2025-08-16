from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
                'class': 'form-control mb-1',
                'placeholder': 'Enter First Name',
            }), label="First Name")
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
                'class': 'form-control mb-1',
                'placeholder': 'Enter Last Name',
            }), label="Last Name")
    username = forms.CharField(max_length=20, widget=forms.TextInput(attrs={
                'class': 'form-control mb-1',
                'placeholder': 'Enter Username',
            }), label="Username")
    email = forms.EmailField(widget=forms.EmailInput(attrs={
                'class': 'form-control mb-1',
                'placeholder': 'Enter E-Mail',
            }), label="E-Mail")
    password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
                'class': 'form-control mb-1',
                'placeholder': 'Enter Password',
            }), label="Password")
    password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
                'class': 'form-control mb-1',
                'placeholder': 'Confirm Password',
            }), label="Confirm Password")
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
        
    def clean_email(self):
        email = self.cleaned_data["email"]
        users = get_user_model()
        
        if users.objects.filter(email=email).exists():
            raise ValidationError(f'Entered email {email} already used in the database, please use another one')
        
        return email

        
        

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control mb-1'}))
    
    password = forms.CharField(max_length=50,
                               required=True,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control mb-1'}))
    
    remember_me = forms.BooleanField(required=False)
    
    class Meta:
        model = User
        fields = ["username", "password", "remember_me"]
        
        
        
class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput())
    
    email = forms.EmailField(required=True,
                             widget=forms.TextInput())
    
    class Meta:
        model = User
        fields = ['username', 'email']
        

class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput())
    bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}))
    
    class Meta:
        model = Profile
        fields = ['avatar', 'bio']
        