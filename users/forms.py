from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(UserCreationForm):
	email=forms.EmailField()
	password1=forms.CharField(label="Hasło",widget=forms.PasswordInput)
	password2=forms.CharField(label="Powtórz Hasło",widget=forms.PasswordInput)
	class Meta:
		model= User
		fields= ['username','email','password1','password2']	
		help_texts = {
            'username': None,
        }
		labels = {
			'username': 'Login',
			'email': 'Email',
		}