from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms

User = get_user_model()

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, help_text='Required', widget=forms.EmailInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
