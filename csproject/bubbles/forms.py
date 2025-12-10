from django import forms
from django.forms import ModelForm
from .models import User, Bubble
        
class RegistrationForm(ModelForm):
    
    password = forms.CharField(widget = forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'password']

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and len(username) < 3:
            self.add_error('username', 'Username should be at least 3 characters long.')
            
        if User.objects.filter(username__iexact=username).exists():
            self.add_error('username', 'Username already in use.')
            
        if password and len(password) < 5:
            self.add_error('password', 'Password should be at least 5 characters long.')

        return cleaned_data
    
class LoginForm(forms.Form):
    
    username = forms.CharField()
    password = forms.CharField(widget = forms.PasswordInput)
        
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        
        if not User.objects.filter(username__iexact=username).exists():
            self.add_error('username', 'User not found')
            
        if User.objects.filter(username=username).exists() and not User.objects.filter(username=username, password=password).exists():
            self.add_error('password', 'Password incorrect')

        return cleaned_data
    
class ChangePwForm(ModelForm):
    
    password = forms.CharField(widget = forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['password']
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')

        if password and len(password) < 5:
            self.add_error('password', 'Password should be at least 5 characters long.')
            
class PostForm(ModelForm):
    
    bubble_text = forms.CharField(widget=forms.Textarea(attrs={'rows':'5', 
                                                               'cols':'42',
                                                               'placeholder':"What's on your mind?"}))
    
    class Meta:
        model = Bubble
        fields = ['bubble_text']
        
        